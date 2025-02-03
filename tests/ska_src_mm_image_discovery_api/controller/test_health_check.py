import pytest
from starlette.responses import JSONResponse
from src.ska_src_mm_image_discovery_api.controller.health_check import HealthCheckController
from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig


@pytest.mark.asyncio
class TestHealthCheckController:


    @pytest.fixture()
    def mock_mongo_client_up(self , mocker):
        mock_mongo = mocker.patch ('src.ska_src_mm_image_discovery_api.config.mongo_config.MongoClient')
        mock_mongo_instance = mock_mongo.return_value
        mock_mongo_instance.server_info.return_value = {"ok": 1}
        return mock_mongo_instance

    @pytest.fixture()
    def mock_mongo_client_down(self , mocker):
        mock_mongo = mocker.patch ('src.ska_src_mm_image_discovery_api.config.mongo_config.MongoClient')
        mock_mongo_instance = mock_mongo.return_value
        mock_mongo_instance.server_info.return_value = {"ok":0}
        return mock_mongo_instance


    async def test_ping_up(self , mock_mongo_client_up):
        controller = HealthCheckController()
        response = await controller.ping()
        assert response.status_code == 200
        assert response.body == b'{"status":"UP","version":null,"mongo_connection":"UP"}'

    # async def test_ping_down(self , mock_mongo_client_down):
    #     controller = HealthCheckController()
    #     response = await controller.ping()
    #     assert response.status_code == 200
    #     assert response.body == b'{"status":"UP","version":null,"mongo_connection":"DOWN"}'
