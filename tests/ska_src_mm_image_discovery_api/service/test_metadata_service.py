import base64
import json
import logging
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository
from src.ska_src_mm_image_discovery_api.service.metadata_service import MetadataService


@pytest.mark.asyncio
class TestMetadataService:
    logger = logging.getLogger("uvicorn")

    @pytest.fixture(autouse=True)
    def mongo_repository(self):
        return AsyncMock(spec=MongoRepository.__cls__)

    @pytest.fixture(autouse=True)
    def metadata_service(self, mongo_repository):
        return MetadataService.__cls__(mongo_repository, AsyncMock())

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

    async def test_get_metadata_by_image_id_not_found(self, metadata_service, mongo_repository):
        image_id = 'non_existent_id'

        mongo_repository.get_metadata_by_image_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.get_metadata_by_image_id(image_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Image with id {image_id} not found"
        mongo_repository.get_metadata_by_image_id.assert_called_once_with(image_id)

    async def test_register_metadata(self, metadata_service, mongo_repository):
        image_url = 'image_url'
        annotations = {
            'Name': 'image_id',
            'Author': 'author_name',
            'Types': ['type_1', 'type_2'],
            'Version': '1',
        }

        metadata_service.skopeo.inspect.return_value = {
            'annotations': {
                'org.opencadc.image-metadata': base64.b64encode(json.dumps(annotations).encode('utf-8')),
            },
            'Digest': 'digest'
        }

        image_metadata = ImageMetadata(image_id='image_id',
                                       author_name='author_name',
                                       types=['type_1', 'type_2'],
                                       digest='digest',
                                       tag='1')

        mongo_repository.register_image_metadata.return_value = image_metadata
        result = await metadata_service.register_metadata(image_url)

        assert result == image_metadata

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        mongo_repository.register_image_metadata.assert_called_once_with(image_metadata)

    async def test_register_metadata_no_annotation_key(self, metadata_service, mongo_repository):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.return_value = {}

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Image metadata not found for image {image_url}"

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        mongo_repository.register_image_metadata.assert_not_called()

    async def test_register_metadata_no_metadata_key(self, metadata_service, mongo_repository):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.return_value = {
            'annotations': {}
        }

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Image metadata not found for image {image_url}"

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        mongo_repository.register_image_metadata.assert_not_called()

    async def test_register_metadata_no_digest_key(self, metadata_service, mongo_repository):
        image_url = 'image_url'
        annotations = {
            'Name': 'image_id',
            'Author': 'author_name',
            'Types': ['type_1', 'type_2'],
            'Version': '1',
        }

        metadata_service.skopeo.inspect.return_value = {
            'annotations': {
                'org.opencadc.image-metadata': base64.b64encode(json.dumps(annotations).encode('utf-8')),
            }
        }

        image_metadata = ImageMetadata(image_id='image_id',
                                       author_name='author_name',
                                       types=['type_1', 'type_2'],
                                       digest='DEFAULT_DIGEST',
                                       tag='1')

        mongo_repository.register_image_metadata.return_value = image_metadata
        result = await metadata_service.register_metadata(image_url)

        assert result == image_metadata

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        mongo_repository.register_image_metadata.assert_called_once_with(image_metadata)

    async def test_register_metadata_skopeo_inspect_failure(self, metadata_service, mongo_repository):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.side_effect = HTTPException(status_code=500, detail="Error while fetching metadata")

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Error while fetching metadata"

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        mongo_repository.register_image_metadata.assert_not_called()
