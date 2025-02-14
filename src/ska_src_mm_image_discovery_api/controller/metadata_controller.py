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

    async def get_image_metadata_list(self, query_params: dict) -> JSONResponse:
        if query_params.get('image_id') is not None:
            metadata = await self.metadata_service.get_metadata_by_image_id(query_params.get('image_id'))
            return JSONResponse(content=jsonable_encoder(metadata))
        metadata_list = await self.metadata_service.get_all_metadata(query_params)
        return JSONResponse(content=jsonable_encoder(metadata_list))

    async def register_image(self, query_params: dict) -> JSONResponse:
        metadata = await self.metadata_service.register_metadata(query_params.get('image_url'))
        return JSONResponse(content=jsonable_encoder(metadata))
