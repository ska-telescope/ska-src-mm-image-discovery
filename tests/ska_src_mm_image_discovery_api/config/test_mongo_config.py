import pytest
from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig


class TestMongoConfig:
    @pytest.fixture()
    def mongo_config_sync(self):
        return MongoConfig(async_mode=False)

    @pytest.fixture()
    def mongo_config_async(self):
        return MongoConfig(async_mode=True)

    def test_connection_sync(self, mocker, mongo_config_sync):
        mock_client = mocker.patch('src.ska_src_mm_image_discovery_api.config.mongo_config.MongoClient')
        mock_client_instance = mock_client.return_value

        mongo_config_sync.connect()

        mock_client.assert_called_once_with(mongo_config_sync.uri)
        assert mongo_config_sync.client is mock_client_instance
        assert mongo_config_sync.db is mock_client_instance[mongo_config_sync.db_name]
        mongo_config_sync.close()

    @pytest.mark.asyncio
    async def test_connection_async(self, mocker, mongo_config_async):
        mock_async_client = mocker.patch('src.ska_src_mm_image_discovery_api.config.mongo_config.AsyncIOMotorClient')
        mock_async_client_instance = mock_async_client.return_value

        mongo_config_async.connect()

        mock_async_client.assert_called_once_with(mongo_config_async.uri)
        assert mongo_config_async.async_client is mock_async_client_instance
        assert mongo_config_async.db is mock_async_client_instance[mongo_config_async.db_name]
        mongo_config_async.close()

    def test_close_sync(self, mocker, mongo_config_sync):
        mock_sync_client = mocker.patch("src.ska_src_mm_image_discovery_api.config.mongo_config.MongoClient")
        mock_sync_client_instance = mock_sync_client.return_value

        mongo_config_sync.connect()
        mongo_config_sync.close()

        assert mock_sync_client_instance.close.call_count == 1

    @pytest.mark.asyncio
    async def test_close_async(self, mocker, mongo_config_async):
        mock_async_client = mocker.patch("src.ska_src_mm_image_discovery_api.config.mongo_config.AsyncIOMotorClient")
        mock_async_client_instance = mock_async_client.return_value

        mongo_config_async.connect()
        mongo_config_async.close()

        assert mock_async_client_instance.close.call_count == 1

    def test_check_connection_sync(self, mocker , mongo_config_sync):
        mock_sync_client = mocker.patch("src.ska_src_mm_image_discovery_api.config.mongo_config.MongoClient")
        mock_sync_client_instance = mock_sync_client.return_value
        mock_sync_client_instance.server_info.return_value = {"ok": 1}

        mongo_config_sync.connect()
        assert mongo_config_sync.check_connection() == "UP"

    @pytest.mark.asyncio
    async def test_check_connection_async(self, mocker , mongo_config_async):
        mock_async_client = mocker.patch("src.ska_src_mm_image_discovery_api.config.mongo_config.AsyncIOMotorClient")
        mock_async_client_instance = mock_async_client.return_value
        mock_async_client_instance.server_info.return_value = {"ok": 1}

        mongo_config_async.connect()
        assert mongo_config_async.check_connection() == "UP"

