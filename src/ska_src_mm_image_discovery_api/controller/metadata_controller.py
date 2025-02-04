from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.service.metadata_service import MetadataService


@singleton
class MetadataController:

    def __init__(self, metadata_service: MetadataService):
        self.metadata_service = metadata_service

    async def get_image_metadata_list(self):
        metadata_list = await self.metadata_service.get_all_metadata()
        return JSONResponse(metadata_list)
