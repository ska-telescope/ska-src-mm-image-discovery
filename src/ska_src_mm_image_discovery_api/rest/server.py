import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version
from starlette.responses import JSONResponse

# from src.ska_src_mm_image_discovery_api.controller.health_check import HealthCheckController
# from src.ska_src_mm_image_discovery_api.decorators import handle_exceptions

app = FastAPI()

# health_check_controller = HealthCheckController()

CORSMiddleware_params = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}
@app.get('/ping')
# @handle_exceptions
@version(1)
async def ping():
    """ Service aliveness. """
    return JSONResponse({
        'status': "UP",
        'version': os.environ.get('SERVICE_VERSION'),
    })



app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')
app.add_middleware(CORSMiddleware, **CORSMiddleware_params)