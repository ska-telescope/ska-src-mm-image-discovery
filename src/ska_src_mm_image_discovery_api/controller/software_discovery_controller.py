import logging

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.service.software_discovery_service import SoftwareDiscoveryService


@singleton
class SoftwareDiscoveryController:
    logger = logging.getLogger("uvicorn")

    def __init__(self, software_discovery_service: SoftwareDiscoveryService):
        self.software_discovery_service = software_discovery_service

    async def discover_software(self, software_type: str, software_name: str | None) -> JSONResponse:
        software_metadata_list = await self.software_discovery_service.get_software_metadata(software_type,
                                                                                             software_name)
        return JSONResponse(content=jsonable_encoder(software_metadata_list, exclude_none=True))

    async def register_software(self) -> JSONResponse:
        return await self.software_discovery_service.register_software_metadata()

    async def update_software(self) -> JSONResponse:
        raise await self.software_discovery_service.update_software_metadata()

    async def delete_software(self) -> JSONResponse:
        raise await self.software_discovery_service.delete_software_metadata()
