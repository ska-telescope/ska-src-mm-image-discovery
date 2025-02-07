import logging

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.service.metadata_service import MetadataService

logger = logging.getLogger("uvicorn")

@singleton
class MetadataController:
    logger = logging.getLogger("uvicorn")
    def __init__(self, metadata_service: MetadataService):
        self.metadata_service = metadata_service

    async def get_image_metadata_list(self) -> JSONResponse:
        metadata_list = await self.metadata_service.get_all_metadata()
        return JSONResponse(content=jsonable_encoder(metadata_list))

    async def get_image_metadata_list_by_type(self , type_name : str) -> JSONResponse :
        metadata_list = await self.metadata_service.get_all_metadata_by_type(type_name)
        return JSONResponse(content=jsonable_encoder(metadata_list))

    async def get_image_metadata_by_image_id(self , image_id : str) -> JSONResponse :
        metadata = await self.metadata_service.get_metadata_by_image_id(image_id)
        return JSONResponse(content=jsonable_encoder(metadata))