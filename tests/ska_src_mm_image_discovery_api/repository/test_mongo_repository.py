import logging
from unittest.mock import AsyncMock, Mock

import pytest
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import ConnectionFailure

from src.ska_src_mm_image_discovery_api.config.mongo_config import MongoConfig
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@pytest.mark.asyncio
class TestMongoRepository:
    logger = logging.getLogger("uvicorn")

    @pytest.fixture(autouse=True)
    def mongo_collection(self):
        mock_collection = AsyncMock(spec=AsyncCollection)
        return mock_collection

    @pytest.fixture(autouse=True)
    def mongo_db(self, mongo_collection):
        mock_db = AsyncMock(spec=AsyncDatabase)
        mock_db.__getitem__.return_value = mongo_collection
        return mock_db

    @pytest.fixture(autouse=True)
    def async_mongo_client(self, mongo_db):
        mongo_client = AsyncMock(spec=AsyncMongoClient)
        mongo_client.__getitem__.return_value = mongo_db
        return mongo_client

    @pytest.fixture(autouse=True)
    def mongo_config(self):
        return MongoConfig(uri="mongodb",
                           metadata_db="test_db",
                           metadata_collections={'images': 'images',
                                                 'docker-container': 'docker-container',
                                                 'jupyter-notebook': 'jupyter-notebook'}
                           )

    @pytest.fixture(autouse=True)
    def mongo_repository(self, mongo_config, async_mongo_client):
        return MongoRepository.__cls__(mongo_config, async_mongo_client)

    async def test_ping_success(self, mongo_repository, async_mongo_client):
        async_mongo_client.admin = AsyncMock()
        async_mongo_client.admin.command = AsyncMock(return_value={'ok': 1})

        await mongo_repository.ping()

        async_mongo_client.admin.command.assert_called_once_with('ping')

    async def test_ping_failure(self, mongo_repository, async_mongo_client):
        async_mongo_client.admin = AsyncMock()
        async_mongo_client.admin.command = AsyncMock(side_effect=ConnectionFailure("Test error"))

        with pytest.raises(Exception) as exc_info:
            await mongo_repository.ping()

        assert "Could not connect to MongoDB" in str(exc_info.value)

    async def test_connection_status_up(self, mongo_repository, async_mongo_client):
        async_mongo_client.server_info = AsyncMock(return_value={'ok': 1})

        status = await mongo_repository.connection_status()

        assert status == "UP"
        async_mongo_client.server_info.assert_called_once()

    async def test_connection_status_down(self, mongo_repository, async_mongo_client):
        async_mongo_client.server_info = AsyncMock(return_value={'ok': 0})

        status = await mongo_repository.connection_status()

        assert status == "DOWN"
        async_mongo_client.server_info.assert_called_once()

    async def test_get_all_metadata(self, mongo_repository, async_mongo_client, mongo_collection):
        find_result = Mock()
        mongo_collection.find.return_value = find_result
        find_result.to_list = AsyncMock(return_value=[{'image_id': '5', 'type_name': 'test'}])

        result = await mongo_repository.get_all_image_metadata({})

        assert result == [{'image_id': '5', 'type_name': 'test'}]
        mongo_collection.find.assert_called_once_with({})
        mongo_collection.find().to_list.assert_called_once_with(length=None)

    async def test_get_all_metadata_with_type(self, mongo_repository, async_mongo_client, mongo_collection):
        find_result = Mock()
        mongo_collection.find.return_value = find_result
        find_result.to_list = AsyncMock(return_value=[{'image_id': '5', 'type_name': 'test'}])

        result = await mongo_repository.get_all_image_metadata({'type_name': 'test'})

        assert result == [{'image_id': '5', 'type_name': 'test'}]
        mongo_collection.find.assert_called_once_with({'type_name': 'test'})
        mongo_collection.find().to_list.assert_called_once_with(length=None)

    async def test_get_metadata_by_image_id_success(self, mongo_repository, async_mongo_client, mongo_collection):
        mongo_collection.find_one.return_value = {'image_id': '6', 'type_name': 'test'}
        image_id = '6'

        result = await mongo_repository.get_image_metadata_by_image_id(image_id)

        assert result == {'image_id': '6', 'type_name': 'test'}
        mongo_collection.find_one.assert_called_once_with({'image_id': image_id})

    async def test_register_image_metadata_success(self , mongo_repository , async_mongo_client , mongo_collection):
        image_metadata = ImageMetadata(image_id='1', name='name', author_name='author_1', types=['type_1'],
                                       digest='digest_1', tag='1')

        return_value = await mongo_repository.register_image_metadata(image_metadata)

        mongo_collection.update_one.assert_called_once_with({'image_id': '1'}, {'$set': image_metadata.__dict__}, upsert=True)
        assert return_value == {'image_id': '1', 'name': 'name', 'author_name': 'author_1', 'types': ['type_1'],
                                'digest': 'digest_1', 'tag': '1'}
