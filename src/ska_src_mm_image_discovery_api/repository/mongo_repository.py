from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class MongoRepository:

    def __init__(self, mongo_config: MongoConfig, mongo_client: AsyncMongoClient):
        self.client = mongo_client
        self.db = self.client[mongo_config.DB]
        self.collection = self.db[mongo_config.Collection]

    async def ping(self):
        try:
            # Explicitly connect to the MongoDB server
            # await self.client.aconnect()
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")

        except ConnectionFailure as e:
            raise Exception(f"Could not connect to MongoDB: {e}")

    async def connection_status(self) -> str:
        server_info = await self.client.server_info()
        return "UP" if server_info.get("ok") == 1 else "DOWN"

    async def get_all_metadata(self):
        metadata_list = []
        async for cursor in self.collection.find():
            metadata_list.append(cursor)
        return metadata_list