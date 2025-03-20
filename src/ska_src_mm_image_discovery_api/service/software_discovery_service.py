import logging

from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.software_metadata import SoftwareMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class SoftwareDiscoveryService:
    logger = logging.getLogger('uvicorn')

    def __init__(self, mongo_config: MongoConfig, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository
        self.mongo_config = mongo_config

    async def get_software_metadata(self, software_type: str, software_name: str | None) -> list[SoftwareMetadata]:
        if not self.mongo_config.is_valid_software_type(software_type):
            raise HTTPException(status_code=404, detail=f"Software type {software_type} not found")
        software_metadata_documents = await self.mongo_repository.get_software_metadata(software_type, software_name)
        software_metadata_list = [SoftwareMetadata(**document) for document in software_metadata_documents]
        return software_metadata_list


    async def register_software_metadata(self) -> JSONResponse:
        raise HTTPException(status_code=501, detail="Not Implemented")

    async def update_software_metadata(self) -> JSONResponse:
        raise HTTPException(status_code=501, detail="Not Implemented")

    async def delete_software_metadata(self) -> JSONResponse:
        raise HTTPException(status_code=501, detail="Not Implemented")
