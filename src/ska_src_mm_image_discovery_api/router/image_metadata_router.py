import logging

from fastapi import APIRouter , Depends
from fastapi_versioning import version
from src.ska_src_mm_image_discovery_api.rest.dependency import get_metadata_controller
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions

image_metadata_router = APIRouter(
    tags =["Image Metadata"],
    prefix= "/image"
)


#todo Route can be changed. Should image_id be image_location?
@image_metadata_router.get('/fetch-one', response_model=ImageMetadata)
@version(1)
@handle_exceptions
async def image_search_with_id(image_id: str, metadata_controller=Depends(get_metadata_controller)):
    """ Get image metadata by image location"""
    return await metadata_controller.get_image_metadata_by_image_location({
        'image_id': image_id
    })


@image_metadata_router.get('/query' , response_model=list[ImageMetadata])
@version(1)
@handle_exceptions
async def image_search(
        type_name: str | None = None,
        metadata_controller=Depends(get_metadata_controller)
):
    """ Get an image metadata list """
    return await metadata_controller.get_image_metadata_list({
        'type_name': type_name,
    })


@image_metadata_router.get('/inspect',  response_model=ImageMetadata)
@version(1)
@handle_exceptions
async def image_inspect(image_url: str, metadata_controller=Depends(get_metadata_controller)):
    """ inspect the entire image metadata """
    return await metadata_controller.image_inspect(image_url)


@image_metadata_router.post('/register', response_model=ImageMetadata)
@version(1)
@handle_exceptions
async def image_register(image_url: str, metadata_controller=Depends(get_metadata_controller)):
    """ Register image metadata """
    return await metadata_controller.register_image({
        'image_url': image_url
    })

