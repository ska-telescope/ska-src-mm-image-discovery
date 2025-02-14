import json
import logging
import base64
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.common.command_executor import CommandExecutor
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class MetadataService:
    logger = logging.getLogger("uvicorn")

    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    async def get_all_metadata(self, metadata_filter: dict) -> list[ImageMetadata]:
        metadata_filter = {"types": metadata_filter.get('type_name')} if metadata_filter.get(
            'type_name') is not None else {}
        image_metadata_list = []
        documents = await self.mongo_repository.get_all_metadata(metadata_filter)
        for document in documents:
            image_metadata = ImageMetadata(**document)
            image_metadata_list.append(image_metadata)
        return image_metadata_list

    async def get_metadata_by_image_id(self, image_id: str) -> ImageMetadata:
        document = await self.mongo_repository.get_metadata_by_image_id(image_id)
        if document is None:
            self.logger.error(f"Image with id {image_id} not found")
            raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found")
        return ImageMetadata(**document)


    async def register_metadata(self, image_url: str) -> ImageMetadata:
        try:
            ## TODO - this can be a responsibility of Skepeo class.
            result = CommandExecutor(f"skopeo inspect {image_url}").execute()
        except Exception as err:
            self.logger.error(f"Error while fetching metadata for image {image_url}", err)
            raise HTTPException(status_code=500, detail=f"Error while fetching metadata for image {image_url}")

        image_metadata = await self.__parse_metadata(result)
        self.logger.info(f"Registering image metadata for image {image_metadata.image_id}")
        
        return await self.mongo_repository.register_image_metadata(image_metadata)


    async def __parse_metadata(self, encoded_data) -> ImageMetadata:
        result_dict = json.loads(encoded_data)

        annotations = result_dict.get('annotations', {})
        annotations_dict = json.loads(annotations)

        ## TODO - keys can vary, need to handle this
        decoded_metadata = self.__decode_metadata(annotations_dict.get("image.metadata"))

        return ImageMetadata(
            image_id=decoded_metadata.get("image_id"),
            author_name=decoded_metadata.get('author', None),
            types=decoded_metadata.get("types", []),
            digest=result_dict.get("Digest", None),
            tag=decoded_metadata.get("tag", None)
        )


    ## TODO - this method can be moved to different class
    @staticmethod
    def __decode_metadata(encoded_data) -> dict:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        return json.loads(decoded_data)
