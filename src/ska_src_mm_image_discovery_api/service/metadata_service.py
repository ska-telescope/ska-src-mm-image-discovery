import base64
import json
import logging

from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.common.skopeo import Skopeo
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class MetadataService:
    logger = logging.getLogger("uvicorn")

    def __init__(self, mongo_repository: MongoRepository, skopeo: Skopeo):
        self.skopeo = skopeo
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
        result = await self.skopeo.inspect(image_url)
        ANNOTATIONS = "Labels"
        IMAGE_METADATA = "annotations"
        DIGEST = "Digest"

        if ANNOTATIONS not in result or IMAGE_METADATA not in result.get(ANNOTATIONS):
            self.logger.error(f"Image metadata not found for image {image_url}")
            raise HTTPException(status_code=404, detail=f"Image metadata not found for image {image_url}")

        ## TODO - keys can vary, need to handle this, check json loads is required or not
        annotations = result.get(ANNOTATIONS)
        digest = result.get(DIGEST)
        metadata = self.__decode_metadata(annotations.get(IMAGE_METADATA))
        return ImageMetadata(**metadata, digest=digest)


    ## TODO - this method can be moved to different class
    @staticmethod
    def __decode_metadata(encoded_data) -> dict:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        return json.loads(decoded_data)
