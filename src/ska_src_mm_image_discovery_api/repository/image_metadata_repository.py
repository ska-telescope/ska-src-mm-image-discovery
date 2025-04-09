import logging

from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class ImageMetadataRepository:
    logger = logging.getLogger("uvicorn")

    def __init__(self, mongo_repository):
        self.mongo_repository = mongo_repository

    async def get_image_metadata_by_image_id(self, image_id: str):
        metadata = await self.mongo_repository.find_one(collection_name="canfar-images",
                                                        metadata_filter={"image_id": image_id})
        if metadata is None:
            self.logger.error(f"Image with id {image_id} not found")
            raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found")

        return metadata

    async def get_all_image_metadata(self, type_name: str | None):
        metadata = await self.mongo_repository.find(
            collection_name="canfar-images",
            metadata_filter={"types": type_name} if type_name else {}
        )

        if not metadata:
            self.logger.warning(f"No metadata found for type: {type_name}")
            raise HTTPException(status_code=404, detail=f"No metadata found for type: {type_name}")

        return metadata

    async def register_metadata(self, image_metadata):
        await self.mongo_repository.update_one(
            collection_name="canfar-images",
            metadata_filter={"image_id": image_metadata.image_id},
            data=image_metadata
        )

        self.logger.info(f"Updated metadata for image {image_metadata.image_id} is {image_metadata}")
        return image_metadata
