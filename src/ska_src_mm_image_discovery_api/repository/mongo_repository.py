import logging

from fastapi import HTTPException
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.decorators.db_exceptions import handle_db_exceptions
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.software_metadata import SoftwareMetadata


@singleton
class MongoRepository:
    logger = logging.getLogger("uvicorn")

    def __init__(self, mongo_config: MongoConfig, mongo_client: AsyncMongoClient):
        self.client = mongo_client
        self.mongo_config = mongo_config
        self.db = self.client[mongo_config.DB]

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
    async def get_all_image_metadata(self, specification: str | None) -> list:
        try:
            collection_name = self.mongo_config.get_collection_name("docker-container")
            collection = self.db[collection_name]

            criteria = {"metadata.specifications": specification} if specification is not None else {
                "metadata.specifications": {"$exists": True, "$ne": []}}
            self.logger.debug("criteria: %s", criteria)
            metadata_list = await collection.find(criteria).to_list(length=None)
            self.logger.debug("metadata_list: %s", metadata_list)
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
            {'executable.location': {'$in': software_metadata.executable.location}},
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


