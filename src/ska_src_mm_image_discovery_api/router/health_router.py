from fastapi import APIRouter
from fastapi import Depends
from fastapi_versioning import version

from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions
from src.ska_src_mm_image_discovery_api.rest.dependency import get_health_check_controller

health_router = APIRouter(
    tags=["Health Check"]
)
@health_router.get("/health")
@version(1)
@handle_exceptions
async def health(health_check_controller=Depends(get_health_check_controller)):
    """ Service aliveness. """
    return await health_check_controller.health()
