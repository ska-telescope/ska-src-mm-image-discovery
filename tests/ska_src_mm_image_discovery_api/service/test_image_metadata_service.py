import base64
import json
import logging
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.config.oci_config import OciConfig
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.models.software_metadata import SoftwareMetadata, Resources, Metadata, \
    Executable, ResourceLimit
from src.ska_src_mm_image_discovery_api.service.image_metadata_service import ImageMetadataService


@pytest.mark.asyncio
class TestMetadataService:
    logger = logging.getLogger("uvicorn")

    @pytest.fixture(autouse=True)
    def metadata_service(self):
        oci_labels_config = OciConfig.__cls__({
            'annotations': 'annotations',
            'metadata': 'org.opencadc.image.metadata',
            'digest': 'Digest'
        }, default_oci_resource={
            "cores": {
                "min": 5,
                "max": 15
            },
            "memory": {
                "min": 3,
                "max": 9
            }
        })
        return ImageMetadataService.__cls__(oci_labels_config, AsyncMock(), AsyncMock())

    async def test_get_all_metadata(self, metadata_service):
        expected_metadata = [
            ImageMetadata(image_id='images.canfar.net/canfar/base-3.11:v0.4.1', name='base-3.11:v0.4.1',
                          author_name='majorb',
                          types=["headless"],
                          digest='sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8',
                          tag='v0.4.1'),
        ]

        metadata_service.image_metadata_repository.get_all_image_metadata.return_value = [{
            "_id": {"$oid": "67f4f834d73d83fdccf87e5c"},
            "author_name": "majorb",
            "digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
            "image_id": "images.canfar.net/canfar/base-3.11:v0.4.1",
            "name": "base-3.11:v0.4.1",
            "tag": "v0.4.1",
            "types": ["headless"]},
        ]

        result = await metadata_service.get_all_image_metadata("type_1")

        assert result == expected_metadata
        metadata_service.image_metadata_repository.get_all_image_metadata.assert_called_once_with("type_1")

    async def test_get_all_metadata_by_type(self, metadata_service):
        expected_metadata = [
            ImageMetadata(image_id='images.canfar.net/canfar/base-3.11:v0.4.1', name='base-3.11:v0.4.1',
                          author_name='majorb',
                          types=["headless"],
                          digest='sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8',
                          tag='v0.4.1'),
        ]

        metadata_service.image_metadata_repository.get_all_image_metadata.return_value = [{
            "_id": {"$oid": "67f4f834d73d83fdccf87e5c"},
            "author_name": "majorb",
            "digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
            "image_id": "images.canfar.net/canfar/base-3.11:v0.4.1",
            "name": "base-3.11:v0.4.1",
            "tag": "v0.4.1",
            "types": ["headless"]},
        ]

        result = await metadata_service.get_all_image_metadata('type_1')

        assert result == expected_metadata
        metadata_service.image_metadata_repository.get_all_image_metadata.assert_called_once_with('type_1')

    async def test_get_metadata_by_image_id(self, metadata_service):
        image_id = 'images.canfar.net/canfar/base-3.11:v0.4.1'
        expected_metadata = ImageMetadata(image_id='images.canfar.net/canfar/base-3.11:v0.4.1', name='base-3.11:v0.4.1',
                                          author_name='majorb',
                                          types=["headless"],
                                          digest='sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8',
                                          tag='v0.4.1')

        metadata_service.image_metadata_repository.get_image_metadata_by_image_id.return_value = {
            "_id": {"$oid": "67f4f834d73d83fdccf87e5c"},
            "author_name": "majorb",
            "digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
            "image_id": "images.canfar.net/canfar/base-3.11:v0.4.1",
            "name": "base-3.11:v0.4.1",
            "tag": "v0.4.1",
            "types": ["headless"]
        }

        result = await metadata_service.get_image_metadata_by_image_location(image_id)

        assert result == expected_metadata
        metadata_service.image_metadata_repository.get_image_metadata_by_image_id.assert_called_once_with(image_id)

    async def test_get_metadata_by_image_id_not_found(self, metadata_service):
        image_id = 'non_existent_id'

        metadata_service.image_metadata_repository.get_image_metadata_by_image_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.get_image_metadata_by_image_location(image_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Image with id {image_id} not found"
        metadata_service.image_metadata_repository.get_image_metadata_by_image_id.assert_called_once_with(image_id)

    async def test_register_metadata(self, metadata_service):
        image_url = 'images.canfar.net/canfar/base-3.11:v0.4.2'
        annotations = {
            'Name': 'name-1',
            'Author': 'author_name',
            'Types': ['type_1', 'type_2'],
            'Version': 'v0.4.2',
        }

        metadata_service.skopeo.inspect.return_value = {
            'annotations': {
                'org.opencadc.image.metadata': base64.b64encode(json.dumps(annotations).encode('utf-8')),
            },
            'Digest': 'digest'
        }

        image_metadata = ImageMetadata(image_id=image_url,
                                       name='name-1',
                                       author_name='author_name',
                                       types=['type_1', 'type_2'],
                                       digest='digest',
                                       tag='v0.4.2')

        metadata_service.image_metadata_repository.add_software_metadata.return_value = image_metadata
        result = await metadata_service.register_metadata(image_url)

        assert result == image_metadata

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        metadata_service.image_metadata_repository.register_metadata.assert_called_once_with(image_metadata)

    async def test_register_metadata_no_annotation_key(self, metadata_service):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.return_value = {}

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'annotations not found for the image'

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        metadata_service.image_metadata_repository.register_image_metadata.assert_not_called()

    async def test_register_metadata_no_metadata_key(self, metadata_service):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.return_value = {
            'annotations': {}
        }

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'metadata not found for the image'

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        metadata_service.image_metadata_repository.register_image_metadata.assert_not_called()

    async def test_register_metadata_skopeo_inspect_failure(self, metadata_service):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.side_effect = HTTPException(status_code=500,
                                                                    detail="Error while fetching metadata")

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Error while fetching metadata"

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        metadata_service.image_metadata_repository.register_image_metadata.assert_not_called()

    async def test_inspect_image_metadata(self, metadata_service):
        image_url = 'image_url'
        metadata_service.skopeo.inspect.return_value = {
            'annotations': {
                'org.opencadc.image.metadata': b'eyJOYW1lIjogIm5hbWUtMSIsICJB'
                                               b'dXRob3IiOiAiYXV0aG9yX25hbWUi'
                                               b'LCAiVHlwZXMiOiBbInR5cGVfMSIs'
                                               b'ICJ0eXBlXzIiXSwgIlZlcnNpb24i'
                                               b'OiAidjAuNC4yIn0=',
            },
            'Digest': 'digest'
        }

        result = await metadata_service.inspect_image_metadata(image_url)

        assert result == {'Digest': 'digest',
                          'annotations': {'org.opencadc.image.metadata': b'eyJOYW1lIjogIm5hbWUtMSIsICJB'
                                                                         b'dXRob3IiOiAiYXV0aG9yX25hbWUi'
                                                                         b'LCAiVHlwZXMiOiBbInR5cGVfMSIs'
                                                                         b'ICJ0eXBlXzIiXSwgIlZlcnNpb24i'
                                                                         b'OiAidjAuNC4yIn0='}}
        metadata_service.skopeo.inspect.assert_called_once_with(image_url)