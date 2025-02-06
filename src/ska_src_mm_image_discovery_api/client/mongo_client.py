from pymongo import AsyncMongoClient

from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class MongoClient:
    def __init__(self, mongo_config: MongoConfig):
        self.mongo_client = AsyncMongoClient(mongo_config.URI)

    def CLIENT(self):
        return self.mongo_client
