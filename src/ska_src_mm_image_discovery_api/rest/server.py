import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version
from src.ska_src_mm_image_discovery_api.router.health_router import router as health_router
from src.ska_src_mm_image_discovery_api.router.software_metadata_router import software_metadata_router
from src.ska_src_mm_image_discovery_api.router.image_metadata_router import image_metadata_router


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
app.include_router(image_metadata_router)


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')
app.add_middleware(CORSMiddleware, **CORSMiddleware_params)
