# Desc: Router for software metadata endpoints

from fastapi import APIRouter, Depends
from fastapi_versioning import version

from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions
from src.ska_src_mm_image_discovery_api.models.software_metadata import SoftwareMetadata
from src.ska_src_mm_image_discovery_api.rest.dependency import get_software_discovery_controller

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

software_metadata_router = APIRouter(
    tags=["Software Metadata"],
    prefix="/software",
)


@software_metadata_router.get('/search', response_model=list[SoftwareMetadata],
         description="This api will return the software metadata list by software name and type")
@version(1)
@handle_exceptions
async def discover_software_metadata(software_type: str, software_name: str | None = None,
                                     software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Get a software metadata list """
    return await software_discovery_controller.discover_software(software_type, software_name)


@software_metadata_router.post('/register', response_model=dict, )
@version(1)
@handle_exceptions
async def register_software_metadata(software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Register Software Metadata """
    return await software_discovery_controller.register_software()


@software_metadata_router.put('/update', response_model=dict)
@version(1)
@handle_exceptions
async def update_software_metadata(software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Update Software metadata """
    return await software_discovery_controller.update_software()


@software_metadata_router.delete('/delete', response_model=dict)
@version(1)
@handle_exceptions
async def delete_software_metadata(software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Delete Software metadata """
    return await software_discovery_controller.delete_software()