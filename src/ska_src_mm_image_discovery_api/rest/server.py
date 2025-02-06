import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version

from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.rest.dependency import get_health_check_controller, get_metadata_controller

logger = logging.getLogger("uvicorn")

# create fastApi
app = FastAPI()
CORSMiddleware_params = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}


@app.get('/health', tags=["Health Check"])
@version(1)
@handle_exceptions
async def health(health_check_controller=Depends(get_health_check_controller)):
    """ Service aliveness. """
    return await health_check_controller.health()


@app.get('/image/search', tags=["Image Metadata"], response_model=list[ImageMetadata])
@version(1)
@handle_exceptions
async def image_search(metadata_controller=Depends(get_metadata_controller)):
    """ Get metadata list """
    return await metadata_controller.get_image_metadata_list()


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
app.add_middleware(CORSMiddleware, **CORSMiddleware_params)