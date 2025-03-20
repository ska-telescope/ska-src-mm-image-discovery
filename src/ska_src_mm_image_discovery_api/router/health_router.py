from fastapi import APIRouter
from fastapi_versioning import  version
from fastapi import FastAPI, Depends
from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions
from src.ska_src_mm_image_discovery_api.rest.dependency import get_health_check_controller

router = APIRouter(
    tags=["Health Check"]
)
@router.get("/health")
@version(1)
@handle_exceptions
async def health(health_check_controller=Depends(get_health_check_controller)):
    """ Service aliveness. """
    return await health_check_controller.health()
