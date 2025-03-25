import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

from src.ska_src_mm_image_discovery_api.router.health_router import health_router
from src.ska_src_mm_image_discovery_api.router.image_metadata_router import image_metadata_router
from src.ska_src_mm_image_discovery_api.router.software_metadata_router import software_metadata_router
from src.ska_src_mm_image_discovery_api.router.web_router import web_router

logger = logging.getLogger("uvicorn")

# create fastApi and Add CORS middleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include api routers
app.include_router(health_router)
app.include_router(software_metadata_router)
app.include_router(image_metadata_router)
app = VersionedFastAPI(app, version_format='{major}', prefix_format='/api/v{major}')

# include web router
app.include_router(web_router)
