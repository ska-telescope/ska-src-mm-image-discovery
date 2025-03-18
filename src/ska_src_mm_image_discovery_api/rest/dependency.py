# return a bean of MongoConfig

from fastapi import Depends
from pymongo import AsyncMongoClient

from src.ska_src_mm_image_discovery_api.client.config_client import ConfigClient
from src.ska_src_mm_image_discovery_api.client.mongo_client import MongoClient
from src.ska_src_mm_image_discovery_api.common.skopeo import Skopeo
from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.controller.health_check_controller import HealthCheckController
from src.ska_src_mm_image_discovery_api.controller.metadata_controller import MetadataController
from src.ska_src_mm_image_discovery_api.controller.software_discovery_controller import SoftwareDiscoveryController
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository
from src.ska_src_mm_image_discovery_api.service.image_metadata_service import ImageMetadataService
from src.ska_src_mm_image_discovery_api.service.software_discovery_service import SoftwareDiscoveryService


# return a bean of ConfigClient
def get_config_client() -> ConfigClient:
    return ConfigClient()


def get_mongo_config(
        config_client: ConfigClient = Depends(get_config_client)
) -> MongoConfig:
    return MongoConfig(
        uri=config_client.get_string("database.uri"),
        metadata_db=config_client.get_string("database.name"),
        metadata_collections=config_client.get_dict("database.collections"),
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
) -> ImageMetadataService:
    return ImageMetadataService(mongo_repository, skopeo)


# return a bean of SoftwareDiscoveryService
# need to give the mongo client
def get_software_metadata_service() -> SoftwareDiscoveryService:
    return SoftwareDiscoveryService()


# return a bean of MetadataController
def get_metadata_controller(
        metadata_service: ImageMetadataService = Depends(get_metadata_service)
) -> MetadataController:
    return MetadataController(metadata_service)


# return a bean of SoftwareDiscoveryController
def get_software_discovery_controller(software_discovery_service: SoftwareDiscoveryService = Depends(
    get_software_metadata_service)) -> SoftwareDiscoveryController:
    return SoftwareDiscoveryController(software_discovery_service)


def get_health_check_controller(
        mongo_repository: MongoRepository = Depends(get_mongo_repository)
) -> HealthCheckController:
    return HealthCheckController(mongo_repository)
