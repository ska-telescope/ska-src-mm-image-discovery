from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.image_metadata_repository import ImageMetadataRepository


@pytest.mark.asyncio
class TestImageMetadataRepository:

    @pytest.fixture(autouse=True)
    def image_metadata_repository(self):
        return ImageMetadataRepository.__cls__(AsyncMock())

    async def test_get_image_metadata_by_image_id(self, image_metadata_repository):
        image_id = "images.canfar.net/canfar/base-3.11:v0.4.1"
        expected_metadata = {
            "_id": {"$oid": "67f4f834d73d83fdccf87e5c"},
            "author_name": "majorb",
            "digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
            "image_id": image_id,
            "name": "base-3.11:v0.4.1",
            "tag": "v0.4.1",
            "types": ["headless"]
        }

        image_metadata_repository.mongo_repository.find_one.return_value = expected_metadata

        result = await image_metadata_repository.get_image_metadata_by_image_id(image_id)

        assert result == expected_metadata
        image_metadata_repository.mongo_repository.find_one.assert_called_once_with(
            collection_name="canfar-images",
            metadata_filter={"image_id": image_id}
        )

    async def test_get_image_metadata_by_image_id_not_found(self, image_metadata_repository):
        image_id = "non_existent_image"
        image_metadata_repository.mongo_repository.find_one.return_value = None

        with pytest.raises(HTTPException) as excinfo:
            await image_metadata_repository.get_image_metadata_by_image_id(image_id)

        assert excinfo.value.status_code == 404
        assert str(excinfo.value.detail) == f"Image with id {image_id} not found"
        image_metadata_repository.mongo_repository.find_one.assert_called_once_with(
            collection_name="canfar-images",
            metadata_filter={"image_id": image_id}
        )

    async def test_get_all_image_metadata(self, image_metadata_repository):
        type_name = "type_1"
        expected_metadata = [
            {
                "_id": {"$oid": "67f4f834d73d83fdccf87e5c"},
                "author_name": "majorb",
                "digest": "sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
                "image_id": "images.canfar.net/canfar/base-3.11:v0.4.1",
                "name": "base-3.11:v0.4.1",
                "tag": "v0.4.1",
                "types": ["headless"]
            }
        ]

        image_metadata_repository.mongo_repository.find.return_value = expected_metadata

        result = await image_metadata_repository.get_all_image_metadata(type_name)

        assert result == expected_metadata
        image_metadata_repository.mongo_repository.find.assert_called_once_with(
            collection_name="canfar-images",
            metadata_filter={"types": type_name}
        )

    async def test_get_all_image_metadata_not_found(self, image_metadata_repository):
        type_name = "non_existent_type"
        image_metadata_repository.mongo_repository.find.return_value = []

        with pytest.raises(HTTPException) as excinfo:
            await image_metadata_repository.get_all_image_metadata(type_name)

        assert excinfo.value.status_code == 404
        assert str(excinfo.value.detail) == f"No metadata found for type: {type_name}"
        image_metadata_repository.mongo_repository.find.assert_called_once_with(
            collection_name="canfar-images",
            metadata_filter={"types": type_name}
        )

    async def test_register_metadata(self, image_metadata_repository):
        image_metadata = ImageMetadata(
            image_id="images.canfar.net/canfar/base-3.11:v0.4.1",
            name="base-3.11:v0.4.1",
            author_name="majorb",
            types=["headless"],
            digest="sha256:d3a1bfad817a2208752e1722c67dcbfad9510f0b4fd21f529af75bd8fb3b0ac8",
            tag="v0.4.1"
        )

        image_metadata_repository.mongo_repository.update_one.return_value = image_metadata

        result = await image_metadata_repository.register_metadata(image_metadata)

        assert result == image_metadata
        image_metadata_repository.mongo_repository.update_one.assert_called_once_with(
            collection_name="canfar-images",
            metadata_filter={"image_id": image_metadata.image_id},
            data=image_metadata
        )
