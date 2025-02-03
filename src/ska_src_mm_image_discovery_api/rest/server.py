from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version
from dotenv import load_dotenv

from src.ska_src_mm_image_discovery_api.controller.health_check import HealthCheckController
from src.ska_src_mm_image_discovery_api.decorators.exceptions import handle_exceptions

load_dotenv()
app = FastAPI()

health_check_controller = HealthCheckController()

CORSMiddleware_params = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}


@app.get('/ping')
@version(1)
@handle_exceptions
async def ping():
    """ Service aliveness. """
    return await health_check_controller.ping()


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
app.add_middleware(CORSMiddleware, **CORSMiddleware_params)