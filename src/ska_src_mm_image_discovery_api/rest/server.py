import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version
from pymongo import AsyncMongoClient

from src.ska_src_mm_image_discovery_api.controller.health_check import HealthCheckController
from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions
from src.ska_src_mm_image_discovery_api.models.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository

logger = logging.getLogger("uvicorn")

# create fastApi
app = FastAPI()
CORSMiddleware_params = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

# create health check controller
health_check_controller = HealthCheckController()

# create mongo config
mongo_config = MongoConfig(
    uri=os.getenv('MONGO_URI', 'mongodb://root:password@localhost:27017/?authSource=admin'),
    db_name=os.getenv('MONGO_DB_NAME', 'metadata_db'),
    collection_name=os.getenv('MONGO_COLLECTION_NAME', 'images')
)
logger.info(f"Mongo URI: {mongo_config.URI}")
logger.info(f"Mongo DB Name: {mongo_config.DB}")
logger.info(f"Mongo Collection Name: {mongo_config.Collection}")

mongo_client = AsyncMongoClient(mongo_config.URI)
mongo_repository = MongoRepository(mongo_config, mongo_client)


@app.get('/health', tags=["Health Check"])
@version(1)
@handle_exceptions
async def ping():
    """ Service aliveness. """
    backend_status = await mongo_repository.connection_status()
    return await health_check_controller.ping(backend_status)





app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
app.add_middleware(CORSMiddleware, **CORSMiddleware_params)