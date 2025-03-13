import logging

from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class SoftwareDiscoveryController:
    logger = logging.getLogger("uvicorn")

    def __init__(self, software_discovery_service):
        self.software_discovery_service = software_discovery_service

    async def discover(self, software_id: str) -> str:
        raise Exception("Not implemented")

    async def register(self) -> str:
        raise Exception("Not implemented")

    async def update(self) -> str:
        raise Exception("Not implemented")

    async def delete(self) -> str:
        raise Exception("Not implemented")
