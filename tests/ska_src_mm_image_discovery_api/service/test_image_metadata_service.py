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
            ImageMetadata(image_id='images.canfar.net/canfar/base-3.11:v0.4.2', name='base-3.11', author_name='majorb',
                          types=[], digest='sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076',
                          tag='v0.4.2'),
        ]

        metadata_service.mongo_repository.get_all_image_metadata.return_value = [
            {
                "_id": {
                    "$oid": "67dab12a88a5719a80afa262"
                },
                "executable": {
                    "location": "images.canfar.net/canfar/base-3.11:v0.4.2",
                    "name": "base-3.11",
                    "type": "docker-container"
                },
                "metadata": {
                    "description": "This is a  base-3.11 image",
                    "version": "v0.4.2",
                    "tag": "v0.4.2",
                    "authorName": "majorb",
                    "digest": "sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076",
                    "specifications": []
                },
                "resources": {
                    "cores": {
                        "min": 5,
                        "max": 15
                    },
                    "memory": {
                        "min": 3,
                        "max": 9
                    }
                }
            }
        ]

        result = await metadata_service.get_all_image_metadata("type_1")

        assert result == expected_metadata
        metadata_service.mongo_repository.get_all_image_metadata.assert_called_once_with('type_1')

    async def test_get_all_metadata_by_type(self, metadata_service):
        expected_metadata = [
            ImageMetadata(image_id='images.canfar.net/canfar/base-3.11:v0.4.2', name='base-3.11', author_name='majorb',
                          types=[], digest='sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076',
                          tag='v0.4.2'),
        ]

        metadata_service.mongo_repository.get_all_image_metadata.return_value = [
            {
                "_id": {
                    "$oid": "67dab12a88a5719a80afa262"
                },
                "executable": {
                    "location": "images.canfar.net/canfar/base-3.11:v0.4.2",
                    "name": "base-3.11",
                    "type": "docker-container"
                },
                "metadata": {
                    "description": "This is a  base-3.11 image",
                    "version": "v0.4.2",
                    "tag": "v0.4.2",
                    "authorName": "majorb",
                    "digest": "sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076",
                    "specifications": []
                },
                "resources": {
                    "cores": {
                        "min": 5,
                        "max": 15
                    },
                    "memory": {
                        "min": 3,
                        "max": 9
                    }
                }
            }
        ]

        result = await metadata_service.get_all_image_metadata('type_1')

        assert result == expected_metadata
        metadata_service.mongo_repository.get_all_image_metadata.assert_called_once_with('type_1')

    async def test_get_metadata_by_image_id(self, metadata_service):
        image_id = '1'
        expected_metadata = ImageMetadata(image_id='images.canfar.net/canfar/base-3.11:v0.4.2', name='base-3.11',
                                          author_name='majorb', types=[],
                                          digest='sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076',
                                          tag='v0.4.2')

        metadata_service.mongo_repository.get_image_metadata_by_location.return_value = {
            "_id": {
                "$oid": "67dab12a88a5719a80afa262"
            },
            "executable": {
                "location": "images.canfar.net/canfar/base-3.11:v0.4.2",
                "name": "base-3.11",
                "type": "docker-container"
            },
            "metadata": {
                "description": "This is a  base-3.11 image",
                "version": "v0.4.2",
                "tag": "v0.4.2",
                "authorName": "majorb",
                "digest": "sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076",
                "specifications": []
            },
            "resources": {
                "cores": {
                    "min": 5,
                    "max": 15
                },
                "memory": {
                    "min": 3,
                    "max": 9
                }
            }
        }

        result = await metadata_service.get_image_metadata_by_image_location(image_id)

        assert result == expected_metadata
        metadata_service.mongo_repository.get_image_metadata_by_location.assert_called_once_with(image_id)

    async def test_get_metadata_by_image_id_not_found(self, metadata_service):
        image_id = 'non_existent_id'

        metadata_service.mongo_repository.get_image_metadata_by_location.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.get_image_metadata_by_image_location(image_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Image with id {image_id} not found"
        metadata_service.mongo_repository.get_image_metadata_by_location.assert_called_once_with(image_id)

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

        software_metadata = SoftwareMetadata(
            executable=Executable(name='name-1', type='docker-container', location=image_url),
            metadata=Metadata(description='This is a docker container with name name-1', version='v0.4.2', tag='v0.4.2',
                              authorName='author_name', digest='digest', specifications=['type_1', 'type_2']),
            resources=Resources(cores=ResourceLimit(min=5, max=15), memory=ResourceLimit(min=3, max=9)), )

        image_metadata = ImageMetadata(image_id=image_url,
                                       name='name-1',
                                       author_name='author_name',
                                       types=['type_1', 'type_2'],
                                       digest='digest',
                                       tag='v0.4.2')

        metadata_service.mongo_repository.add_software_metadata.return_value = image_metadata
        result = await metadata_service.register_metadata(image_url)

        assert result == image_metadata

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        metadata_service.mongo_repository.add_software_metadata.assert_called_once_with("docker-container",
                                                                                        software_metadata)

    async def test_register_metadata_no_annotation_key(self, metadata_service):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.return_value = {}

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'annotations not found for the image'

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        metadata_service.mongo_repository.register_image_metadata.assert_not_called()

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
        metadata_service.mongo_repository.register_image_metadata.assert_not_called()

    async def test_register_metadata_skopeo_inspect_failure(self, metadata_service):
        image_url = 'image_url'

        metadata_service.skopeo.inspect.side_effect = HTTPException(status_code=500,
                                                                    detail="Error while fetching metadata")

        with pytest.raises(HTTPException) as exc_info:
            await metadata_service.register_metadata(image_url)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Error while fetching metadata"

        metadata_service.skopeo.inspect.assert_called_once_with(image_url)
        metadata_service.mongo_repository.register_image_metadata.assert_not_called()
