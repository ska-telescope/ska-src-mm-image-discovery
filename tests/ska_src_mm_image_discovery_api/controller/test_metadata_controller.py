from unittest.mock import AsyncMock
import pytest
import json
from src.ska_src_mm_image_discovery_api.controller.metadata_controller import MetadataController

@pytest.mark.asyncio
class TestMetadataController:

    @pytest.fixture(autouse=True)
    def metadata_controller(self):
        return MetadataController(AsyncMock())

    async def test_get_image_metadata_list_by_type(self, metadata_controller):
        metadata_controller.metadata_service.get_all_metadata.return_value = [
            {
                "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
                "author_name": "mockauthor"
            },
            {
                "image_id": "images.canfar.net/canfar/3.12:v0.1.2",
                "author_name": "mockauthor2"
            }
        ]

        query_params = {"type": "type"}

        response = await metadata_controller.get_image_metadata_list(query_params)
        json_response = json.loads(response.body.decode("utf-8"))

        assert json_response == [
            {
                "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
                "author_name": "mockauthor"
            },
            {
                "image_id": "images.canfar.net/canfar/3.12:v0.1.2",
                "author_name": "mockauthor2"
            }
        ]
        metadata_controller.metadata_service.get_all_metadata.assert_called_once_with(query_params)

    async def test_get_image_metadata_when_image_id_is_present(self, metadata_controller):
        metadata_controller.metadata_service.get_metadata_by_image_id = AsyncMock(return_value={
            "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
            "author_name": "mockauthor"
        })

        query_params = {'image_id': 'image_id'}
        response = await metadata_controller.get_image_metadata_list(query_params)
        json_response = json.loads(response.body.decode("utf-8"))

        assert json_response == {
            "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
            "author_name": "mockauthor"
        }

        metadata_controller.metadata_service.get_metadata_by_image_id.assert_called_once_with("image_id")


    async def test_register_image(self, metadata_controller):
        metadata_controller.metadata_service.register_metadata = AsyncMock(return_value={
            "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
            "author_name": "mockauthor"
        })

        query_params = {'image_url': 'image_url'}
        response = await metadata_controller.register_image(query_params)
        json_response = json.loads(response.body.decode("utf-8"))

        assert json_response == {
            "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
            "author_name": "mockauthor"
        }

        metadata_controller.metadata_service.register_metadata.assert_called_once_with("image_url")