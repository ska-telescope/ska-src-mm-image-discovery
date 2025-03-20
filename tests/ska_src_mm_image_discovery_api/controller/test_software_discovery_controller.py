import json
from unittest.mock import AsyncMock
from src.ska_src_mm_image_discovery_api.controller.software_discovery_controller import SoftwareDiscoveryController

import pytest


class TestSoftwareDiscoverController:

    @pytest.fixture
    def software_discovery_controller(self):
        return SoftwareDiscoveryController(AsyncMock())

    async def test_get_software_metadata(self, software_discovery_controller):
        software_discovery_controller.software_discovery_service.get_software_metadata.return_value = [
            {
                "software_type": "type",
                "software_name": "name"
            },
            {
                "software_type": "type",
                "software_name": "name"
            }
        ]

        software_name = "name"
        software_type = "type"

        response = await software_discovery_controller.discover_software(software_type, software_name)

        json_response = json.loads(response.body.decode("utf-8"))

        assert json_response == [
            {
                "software_type": "type",
                "software_name": "name"
            },
            {
                "software_type": "type",
                "software_name": "name"
            }
        ]

        print(software_discovery_controller.software_discovery_service.get_software_metadata.call_args)

        software_discovery_controller.software_discovery_service.get_software_metadata.assert_called_once_with('type', 'name')
