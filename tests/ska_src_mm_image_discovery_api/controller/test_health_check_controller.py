from unittest.mock import AsyncMock
import pytest
from src.ska_src_mm_image_discovery_api.controller.health_check_controller import HealthCheckController
import json

class TestHealthCheckController:
    @pytest.mark.asyncio
    async def test_health_success(self):
        health_check_controller = HealthCheckController(AsyncMock())
        health_check_controller.mongo_repository.connection_status.return_value = "UP"

        response = await health_check_controller.health()
        json_response = response.body.decode("utf-8")
        json_response = json.loads(json_response)

        assert response.status_code == 200
        assert json_response == {
            'status': "UP",
            'version': None,
            'backend_connection': "UP"
        }

    @pytest.mark.asyncio
    async def test_health_down(self):
        health_check_controller = HealthCheckController(AsyncMock())
        health_check_controller.mongo_repository.connection_status.return_value = "DOWN"

        response = await health_check_controller.health()
        json_response = response.body.decode("utf-8")
        json_response = json.loads(json_response)

        assert response.status_code == 200
        assert json_response == {
            'status': "UP",
            'version': None,
            'backend_connection': "DOWN"
        }
