from unittest.mock import AsyncMock
import pytest
import json
from src.ska_src_mm_image_discovery_api.controller.metadata_controller import MetadataController


class TestMetadataController:
    @pytest.mark.asyncio
    async def test_get_image_metadata_list_by_type(self):
        controller = MetadataController(AsyncMock())

        controller.metadata_service.get_all_metadata.return_value = [
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

        response = await controller.get_image_metadata_list(query_params)
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
        controller.metadata_service.get_all_metadata.assert_called_once_with(query_params)

    @pytest.mark.asyncio
    async def test_get_image_metadata_when_image_id_is_present(self):
        controller = MetadataController(AsyncMock())

        controller.metadata_service.get_metadata_by_image_id = AsyncMock(return_value={
            "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
            "author_name": "mockauthor"
        })

        query_params = {'image_id': 'image_id'}
        response = await controller.get_image_metadata_list(query_params)
        json_response = json.loads(response.body.decode("utf-8"))

        assert json_response == {
            "image_id": "images.canfar.net/canfar/3.12:v0.1.1",
            "author_name": "mockauthor"
        }

        controller.metadata_service.get_metadata_by_image_id.assert_called_once_with("image_id")
