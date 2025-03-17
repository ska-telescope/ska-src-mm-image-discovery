import logging

from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class SoftwareDiscoveryService:
    logger = logging.getLogger('uvicorn')

    def __init__(self):
        pass

    async def get_software_metadata(self) -> JSONResponse:
        raise HTTPException(status_code=501, detail="Not Implemented")

    async def register_software_metadata(self) -> JSONResponse:
        raise HTTPException(status_code=501, detail="Not Implemented")

    async def update_software_metadata(self) -> JSONResponse:
        raise HTTPException(status_code=501, detail="Not Implemented")

    async def delete_software_metadata(self) -> JSONResponse:
        raise HTTPException(status_code=501, detail="Not Implemented")
