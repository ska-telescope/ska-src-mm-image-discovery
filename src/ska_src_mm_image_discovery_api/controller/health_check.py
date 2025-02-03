import os

from starlette.responses import JSONResponse

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig

@singleton
class HealthCheckController:

    def __init__(self):
        self.mongo_config = MongoConfig(async_mode=False)
        self.mongo_config.connect()

    async def ping(self) -> JSONResponse:
        """ Service aliveness. """
        connection_status = self.mongo_config.check_connection()
        return JSONResponse({
            'status': "UP",
            'version': os.environ.get('SERVICE_VERSION'),
            'mongo_connection': connection_status
        })