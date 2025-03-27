import logging
from unittest.mock import Mock, AsyncMock

import pytest
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.models.software_metadata import SoftwareMetadata, Metadata, Executable, \
    ResourceLimit, Resources
from src.ska_src_mm_image_discovery_api.service.software_discovery_service import SoftwareDiscoveryService


@pytest.mark.asyncio
class TestSoftwareDiscoveryService:
    logger = logging.getLogger("uvicorn")

    @pytest.fixture(autouse=True)
    def software_discovery_service(self):
        mongo_config = Mock()
        return SoftwareDiscoveryService.__cls__(mongo_config, AsyncMock())

    async def test_get_software_metadata(self, software_discovery_service):
        software_discovery_service.mongo_config.is_valid_software_type.return_value = True
        software_discovery_service.mongo_repository.get_software_metadata.return_value = [
            {
                "_id": {
                    "$oid": "67dab12a88a5719a80afa262"
                },
                "executable": {
                    "location": ["images.canfar.net/canfar/base-3.11:v0.4.2"],
                    "name": "base-3.11",
                    "type": "docker-container",
                    "digest": "sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076",
                },
                "metadata": {
                    "description": "This is a  base-3.11 image",
                    "version": "v0.4.2",
                    "tag": "v0.4.2",
                    "authorName": "majorb",

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

        software_metadata_list = await software_discovery_service.get_software_metadata("docker-container", "base-3.11")
        assert software_metadata_list == [
            SoftwareMetadata(
                executable=Executable(name='base-3.11', type='docker-container',
                                      location=["images.canfar.net/canfar/base-3.11:v0.4.2"],
                                      digest='sha256:04849f1bd0ac61427745fd6f9c2bf0a9fb3d2fc91335bd0385992210d4bb8076'),
                metadata=Metadata(description='This is a  base-3.11 image', version='v0.4.2', tag='v0.4.2',
                                  authorName='majorb',
                                  specifications=[]),
                resources=Resources(cores=ResourceLimit(min=5, max=15), memory=ResourceLimit(min=3, max=9)), )
        ]

        software_discovery_service.mongo_repository.get_software_metadata.assert_called_once_with("docker-container","base-3.11")


    async def test_get_software_metadata_when_software_type_is_invalid(self, software_discovery_service):
        software_discovery_service.mongo_config.is_valid_software_type.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            await software_discovery_service.get_software_metadata("docker-container", "base-3.11", )

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Software type docker-container not found"
        software_discovery_service.mongo_repository.get_software_metadata.assert_not_called()
