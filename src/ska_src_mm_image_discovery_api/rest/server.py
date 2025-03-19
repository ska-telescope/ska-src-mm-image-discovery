import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version

from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.rest.dependency import get_metadata_controller
from src.ska_src_mm_image_discovery_api.router.health_router import router as health_router
from src.ska_src_mm_image_discovery_api.router.software_metadata_router import software_metadata_router

logger = logging.getLogger("uvicorn")

# create fastApi
app = FastAPI()
CORSMiddleware_params = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

app.include_router(health_router)
app.include_router(software_metadata_router)


#todo -> divide in 2 apis
@app.get('/image/search', tags=["Image Metadata"], response_model=list[ImageMetadata])
@version(1)
@handle_exceptions
async def image_search(
        type_name: str | None = None,
        image_id: str | None = None,
        metadata_controller=Depends(get_metadata_controller)
):
    """ Get metadata list """
    return await metadata_controller.get_image_metadata_list({
        'type_name': type_name,
        'image_id': image_id
    })


@app.get('/image/inspect', tags=["Image Metadata"], response_model=ImageMetadata)
@version(1)
@handle_exceptions
async def image_inspect(image_url: str, metadata_controller=Depends(get_metadata_controller)):
    # """ inspect image metadata """
    return await metadata_controller.image_inspect(image_url)


@app.post('/image/register', tags=["Image Metadata"], response_model=ImageMetadata)
@version(1)
@handle_exceptions
async def image_register(image_url: str, metadata_controller=Depends(get_metadata_controller)):
    # """ Register image metadata """
    return await metadata_controller.register_image({
        'image_url': image_url
    })


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')
app.add_middleware(CORSMiddleware, **CORSMiddleware_params)
