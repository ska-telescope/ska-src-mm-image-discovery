import logging

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.service.image_metadata_service import ImageMetadataService

logger = logging.getLogger("uvicorn")


@singleton
class ImageMetadataController:
    logger = logging.getLogger("uvicorn")

    def __init__(self, metadata_service: ImageMetadataService):
        self.metadata_service = metadata_service

    async def image_inspect(self, image_url: str) -> JSONResponse:
        metadata = await self.metadata_service.inspect_image_metadata(image_url)
        return JSONResponse(content=jsonable_encoder(metadata))

    async def get_image_metadata_list(self, type_name: str | None) -> JSONResponse:
        metadata_list = await self.metadata_service.get_all_image_metadata(type_name)
        return JSONResponse(content=jsonable_encoder(metadata_list))

    async def register_image(self, query_params: dict) -> JSONResponse:
        metadata = await self.metadata_service.register_metadata(query_params.get('image_url'))
        return JSONResponse(content=jsonable_encoder(metadata))

    async def get_image_metadata_by_image_location(self, image_id: str) -> JSONResponse:
        metadata = await self.metadata_service.get_image_metadata_by_image_location(image_id)
        return JSONResponse(content=jsonable_encoder(metadata))
