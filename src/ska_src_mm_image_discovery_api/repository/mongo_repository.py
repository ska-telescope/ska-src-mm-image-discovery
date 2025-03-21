import logging

from fastapi import HTTPException
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.models.software_metadata import SoftwareMetadata
from src.ska_src_mm_image_discovery_api.decorators.db_exceptions import handle_db_exceptions

@singleton
class MongoRepository:
    logger = logging.getLogger("uvicorn")

    def __init__(self, mongo_config: MongoConfig, mongo_client: AsyncMongoClient):
        self.client = mongo_client
        self.mongo_config = mongo_config
        self.db = self.client[mongo_config.DB]
        self.images_collection = self.db[mongo_config.images_collection]

    async def ping(self):
        try:
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except ServerSelectionTimeoutError as e:
            raise HTTPException(status_code=504, detail=f"MongoDB server selection timed out: {e}")
        except ConnectionFailure as e:
            raise HTTPException(status_code=503, detail=f"Could not connect to MongoDB: {e}")

    async def connection_status(self) -> str:
        server_info = await self.client.server_info()
        return "UP" if server_info.get("ok") == 1 else "DOWN"

    @handle_db_exceptions
    async def register_image_metadata(self, image_metadata: ImageMetadata) -> ImageMetadata:
        updated_metadata = await self.images_collection.update_one(
            {'image_id': image_metadata.image_id},
            {'$set': image_metadata.__dict__},
            upsert=True
        )
        self.logger.info(f"Updated metadata for image {image_metadata.image_id} is {updated_metadata}")
        return image_metadata

    @handle_db_exceptions
    async def get_all_image_metadata(self, specification=None) -> list:
        try:
            collection_name = self.mongo_config.get_collection_name("docker-container")
            collection = self.db[collection_name]

            criteria = {"metadata.specifications": specification} if specification is not None else {}
            metadata_list = await collection.find(criteria).to_list(length=None)
            return metadata_list
        except ServerSelectionTimeoutError as e:
            raise TimeoutError(f"MongoDB server selection timed out: {e}")

    @handle_db_exceptions
    async def get_image_metadata_by_location(self, location: str) -> dict:
        collection_name = self.mongo_config.get_collection_name("docker-container")
        collection = self.db[collection_name]
        return await collection.find_one({"executable.location": location})

    @handle_db_exceptions
    async def add_software_metadata(self, software_type: str, software_metadata: SoftwareMetadata) -> SoftwareMetadata:
        collection_name = self.mongo_config.get_collection_name(software_type)
        collection = self.db[collection_name]
        await collection.update_one(
            {'executable.location': software_metadata.executable.location},
            {'$set': software_metadata.dict()},
            upsert=True

        )
        return software_metadata

    @handle_db_exceptions
    async def get_software_metadata(self, software_type: str, software_name: str | None = None) -> list:
        collection_name = self.mongo_config.get_collection_name(software_type)
        collection = self.db[collection_name]
        criteria = {'executable.name': software_name} if software_name is not None else {}
        metadata_list = await collection.find(criteria).to_list(length=None)
        return metadata_list
