import asyncio
import json
import logging

from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.common.command_executor import CommandExecutor
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class Skopeo:
    logger = logging.getLogger("uvicorn")

    def __init__(self):
        pass

    async def inspect(self, image_url: str) -> dict:
        results = await asyncio.gather(
            self.__inspect(image_url, "--tls-verify=false --raw"),
            self.__inspect(image_url, "--tls-verify=false")
        )
        return {**results[0], **results[1]}

    async def __inspect(self, image_url: str, options: str) -> dict:
        try:
            cmd = CommandExecutor(f"skopeo inspect docker://{image_url} {options}")
            result = await cmd.execute()
            return json.loads(result)
        except Exception as err:
            self.logger.error(f"Error while fetching metadata for image {image_url}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error while fetching metadata for image {image_url}")
