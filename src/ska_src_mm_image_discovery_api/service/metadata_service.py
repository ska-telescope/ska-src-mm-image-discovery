import logging

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
        document =  await self.mongo_repository.get_metadata_by_image_id(image_id)
        if document is None:
            self.logger.error(f"Image with id {image_id} not found")
            raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found")
        return ImageMetadata(**document)

    async def register_metadata(self, image_url: str) -> ImageMetadata:
        result, err = CommandExecutor(f"skopeo inspect {image_url}").execute()
        if err:
            self.logger.error(f"Error while fetching metadata for image {image_url}")
            raise HTTPException(status_code=500, detail=f"Error while fetching metadata for image {image_url}")

        self.logger.info(result)
        pass