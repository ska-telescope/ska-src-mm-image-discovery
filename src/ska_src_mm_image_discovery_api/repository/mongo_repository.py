import logging

from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata


@singleton
class MongoRepository:
    logger = logging.getLogger("uvicorn")

    def __init__(self, mongo_config: MongoConfig, mongo_client: AsyncMongoClient):
        self.client = mongo_client
        self.db = self.client[mongo_config.DB]
        self.collection = self.db[mongo_config.Collection]

    async def ping(self):
        try:
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")

        except ConnectionFailure as e:
            raise Exception(f"Could not connect to MongoDB: {e}")

    async def connection_status(self) -> str:
        server_info = await self.client.server_info()
        return "UP" if server_info.get("ok") == 1 else "DOWN"

    async def get_all_metadata(self, metadata_filter: dict) -> list:
        metadata_list = await self.collection.find(metadata_filter).to_list(length=None)
        return metadata_list

    async def get_metadata_by_image_id(self, image_id: str) -> dict:
        return await self.collection.find_one({'image_id': image_id})

    async def register_image_metadata(self, image_metadata: ImageMetadata) -> ImageMetadata:
        updated_metadata = await self.collection.update_one(
            {'image_id': image_metadata.image_id},
            {'$set': image_metadata.__dict__},
            upsert=True
        )
        self.logger.info(f"Updated metadata for image {image_metadata.image_id} is {updated_metadata}")
        return image_metadata

