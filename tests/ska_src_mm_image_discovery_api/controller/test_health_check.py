import pytest

from src.ska_src_mm_image_discovery_api.controller.health_check import HealthCheckController


@pytest.mark.asyncio
class TestHealthCheckController:

    async def test_ping(self):
        controller = HealthCheckController()
        response = await controller.ping()
        assert response.status_code == 200
        assert response.body == b'{"status":"UP","version":null}'
