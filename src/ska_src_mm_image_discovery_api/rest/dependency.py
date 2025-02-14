# return a bean of MongoConfig
import os

from fastapi import Depends
from pymongo import AsyncMongoClient

from src.ska_src_mm_image_discovery_api.client.mongo_client import MongoClient
from src.ska_src_mm_image_discovery_api.common.skopeo import Skopeo
from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.controller.health_check_controller import HealthCheckController
from src.ska_src_mm_image_discovery_api.controller.metadata_controller import MetadataController
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository
from src.ska_src_mm_image_discovery_api.service.metadata_service import MetadataService


def get_mongo_config() -> MongoConfig:
    return MongoConfig(
        uri=os.getenv('MONGO_URI', 'mongodb://root:password@localhost:27017/?authSource=admin'),
        db_name=os.getenv('MONGO_DB_NAME', 'metadata_db'),
        collection_name=os.getenv('MONGO_COLLECTION_NAME', 'images')
    )


# return a bean of AsyncMongoClient
def get_mongo_client(
        mongo_config: MongoConfig = Depends(get_mongo_config)
) -> AsyncMongoClient:
    return MongoClient(mongo_config).CLIENT()


# return a bean of MongoRepository
def get_mongo_repository(
        mongo_config: MongoConfig = Depends(get_mongo_config),
        mongo_client: AsyncMongoClient = Depends(get_mongo_client)
) -> MongoRepository:
    return MongoRepository(mongo_config, mongo_client)


# return a bean of Skopeo
def get_skopeo() -> Skopeo:
    return Skopeo()

# return a bean of MetadataService
def get_metadata_service(
        mongo_repository: MongoRepository = Depends(get_mongo_repository),
        skopeo: Skopeo = Depends(get_skopeo)
) -> MetadataService:
    return MetadataService(mongo_repository, skopeo)


# return a bean of MetadataController
def get_metadata_controller(
        metadata_service: MetadataService = Depends(get_metadata_service)
) -> MetadataController:
    return MetadataController(metadata_service)


def get_health_check_controller(
        mongo_repository: MongoRepository = Depends(get_mongo_repository)
) -> HealthCheckController:
    return HealthCheckController(mongo_repository)
