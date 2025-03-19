# Desc: Router for software metadata endpoints

from fastapi import APIRouter , Depends
from fastapi_versioning import  version
from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions
from src.ska_src_mm_image_discovery_api.rest.dependency import get_software_discovery_controller

software_metadata_router = APIRouter(
    tags=["Software Metadata"],
    prefix="/software",
)


@software_metadata_router.get('/metadata',
         description="This api will return the software metadata list by software name and type")
@version(1)
@handle_exceptions
async def discover_software_metadata(software_name: str, software_type: str,
                                     software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Get software metadata list """
    return await software_discovery_controller.discover_software(software_name, software_type)


@software_metadata_router.post('/register')
@version(1)
@handle_exceptions
async def register_software_metadata(software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Register Software Metadata """
    return await software_discovery_controller.register_software()

@software_metadata_router.put('/update')
@version(1)
@handle_exceptions
async def update_software_metadata(software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Update Software metadata """
    return await software_discovery_controller.update_software()


@software_metadata_router.delete('/delete')
@version(1)
@handle_exceptions
async def delete_software_metadata(software_discovery_controller=Depends(get_software_discovery_controller)):
    """ Delete Software metadata """
    return await software_discovery_controller.delete_software()