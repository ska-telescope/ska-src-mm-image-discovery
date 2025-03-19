import json
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.controller.image_metadata_controller import ImageMetadataController


@pytest.mark.asyncio
class TestImageMetadataController:

    @pytest.fixture(autouse=True)
    def metadata_controller(self):
        return ImageMetadataController(AsyncMock())

    async def test_get_image_metadata_list_by_type(self, metadata_controller):
        metadata_controller.metadata_service.get_all_image_metadata.return_value = [
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
        metadata_controller.metadata_service.get_all_image_metadata.assert_called_once_with(query_params)

    async def test_get_image_metadata_when_image_id_is_present(self, metadata_controller):
        metadata_controller.metadata_service.get_image_metadata_by_image_id = AsyncMock(return_value={
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

        metadata_controller.metadata_service.get_image_metadata_by_image_id.assert_called_once_with("image_id")

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

    async def test_register_image_when_metadata_not_found(self, metadata_controller):
        metadata_controller.metadata_service.register_metadata.side_effect = HTTPException(status_code=404,
                                                                                           detail="Image metadata not found for image image_url")

        query_params = {'image_url': 'image_url'}
        with pytest.raises(HTTPException) as exc_info:
            await metadata_controller.register_image(query_params)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Image metadata not found for image image_url"
