import os

from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class HealthCheckController:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    async def health(self) -> JSONResponse:
        backend_connection = await self.mongo_repository.connection_status()
        """ Service aliveness. """
        return JSONResponse({
            'status': "UP",
            'version': os.environ.get('SERVICE_VERSION'),
            'backend_connection': backend_connection,
        })
