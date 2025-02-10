import logging
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository
from src.ska_src_mm_image_discovery_api.service.metadata_service import MetadataService


class TestMetadataService:
    logger = logging.getLogger("uvicorn")

    @pytest.fixture(autouse=True)
    def mongo_repository(self):
        return AsyncMock(spec=MongoRepository.__cls__)

    @pytest.fixture(autouse=True)
    def metadata_service(self, mongo_repository):
        return MetadataService.__cls__(mongo_repository)

    @pytest.mark.asyncio
    async def test_get_all_metadata(self, metadata_service, mongo_repository):
        metadata_filter = {}
        expected_metadata = [
            ImageMetadata(image_id='1', author_name='author_1', types=list('type_1'), digest='digest_1', tag='1'),
            ImageMetadata(image_id='2', author_name='author_2', types=list('type_2'), digest='digest_2', tag='1')
        ]

        mongo_repository.get_all_metadata.return_value = [
            {'image_id': '1', 'author_name': 'author_1', 'types': list('type_1'), 'digest': 'digest_1', 'tag': '1'},
            {'image_id': '2', 'author_name': 'author_2', 'types': list('type_2'), 'digest': 'digest_2', 'tag': '1'}
        ]

        result = await metadata_service.get_all_metadata(metadata_filter)

        assert result == expected_metadata
        mongo_repository.get_all_metadata.assert_called_once_with(metadata_filter)

    @pytest.mark.asyncio
    async def test_get_all_metadata_by_type(self, metadata_service, mongo_repository):
        metadata_filter = {'type_name': 'type_1'}
        expected_metadata = [
            ImageMetadata(image_id='1', author_name='author_1', types=list('type_1'), digest='digest_1', tag='1'),
        ]

        mongo_repository.get_all_metadata.return_value = [
            {'image_id': '1', 'author_name': 'author_1', 'types': list('type_1'), 'digest': 'digest_1', 'tag': '1'},
        ]

        result = await metadata_service.get_all_metadata(metadata_filter)

        assert result == expected_metadata
        mongo_repository.get_all_metadata.assert_called_once_with({'types': 'type_1'})

    @pytest.mark.asyncio
    async def test_get_metadata_by_image_id(self, metadata_service, mongo_repository):
        image_id = '1'
        expected_metadata = ImageMetadata(image_id='1', author_name='author_1', types=list('type_1'), digest='digest_1',
                                          tag='1')

        mongo_repository.get_metadata_by_image_id.return_value = {'image_id': '1', 'author_name': 'author_1',
                                                                  'types': list('type_1'), 'digest': 'digest_1',
                                                                  'tag': '1'}

        result = await metadata_service.get_metadata_by_image_id(image_id)

        assert result == expected_metadata
        mongo_repository.get_metadata_by_image_id.assert_called_once_with(image_id)

    @pytest.mark.asyncio
    async def test_get_metadata_by_image_id_not_found(self, metadata_service, mongo_repository):
        image_id = 'non_existent_id'

        mongo_repository.get_metadata_by_image_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.get_metadata_by_image_id(image_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Image with id {image_id} not found"
        mongo_repository.get_metadata_by_image_id.assert_called_once_with(image_id)
