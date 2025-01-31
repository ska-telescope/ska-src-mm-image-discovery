import os

from starlette.responses import JSONResponse

from ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class HealthCheckController:

    async def ping(self) -> JSONResponse:
        """ Service aliveness. """
        return JSONResponse({
            'status': "UP",
            'version': os.environ.get('SERVICE_VERSION'),
        })