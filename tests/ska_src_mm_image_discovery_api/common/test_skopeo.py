import json
import logging
from unittest.mock import patch, AsyncMock

import pytest
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.common.command_executor import CommandExecutor
from src.ska_src_mm_image_discovery_api.common.skopeo import Skopeo


@pytest.mark.asyncio
class TestSkopeo:

    @pytest.fixture(autouse=True)
    def skopeo(self):
        return Skopeo()

    @patch.object(CommandExecutor, 'execute', new_callable=AsyncMock)
    async def test_skopeo_inspect_success(self, mock_execute, skopeo):
        mock_execute.side_effect = [
            json.dumps({"key1": "value1"}),
            json.dumps({"key2": "value2"})]

        result = await skopeo.inspect("image_url")
        logging.info(result)
        assert result == {"key1": "value1", "key2": "value2"}


    @patch.object(CommandExecutor, 'execute', new_callable=AsyncMock)
    async def test_inspect_failure(self, mock_execute, skopeo):
        mock_execute.side_effect = Exception("Command failed")
        image_url = "test_image_url"
        with pytest.raises(HTTPException) as exc_info:
            await skopeo.inspect(image_url)
        assert exc_info.value.status_code == 500
        assert "Error while fetching metadata for image" in exc_info.value.detail