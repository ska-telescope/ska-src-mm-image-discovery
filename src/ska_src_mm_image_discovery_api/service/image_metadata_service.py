import base64
import json
import logging

from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.repository.image_metadata_repository import ImageMetadataRepository
from src.ska_src_mm_image_discovery_api.common.skopeo import Skopeo
from src.ska_src_mm_image_discovery_api.config.oci_config import OciConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata


@singleton
class ImageMetadataService:
    logger = logging.getLogger("uvicorn")

    def __init__(self, oci_labels_config: OciConfig, image_metadata_repository: ImageMetadataRepository, skopeo: Skopeo):
        self.oci_labels_config = oci_labels_config
        self.image_metadata_repository = image_metadata_repository
        self.skopeo = skopeo

    async def get_all_image_metadata(self, type_name: str | None) -> list[ImageMetadata]:
        image_metadata_list = []

        documents = await self.image_metadata_repository.get_all_image_metadata(type_name)
        for metadata in documents:
            image_metadata = ImageMetadata(**metadata)
            image_metadata_list.append(image_metadata)

        return image_metadata_list

    async def get_image_metadata_by_image_location(self, image_id: str) -> ImageMetadata:
        metadata = await self.image_metadata_repository.get_image_metadata_by_image_id(image_id)
        if metadata is None:
            self.logger.error(f"Image with id {image_id} not found")
            raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found")

        return ImageMetadata(**metadata)

    async def inspect_image_metadata(self, image_url: str) -> dict:
        return await self.skopeo.inspect(image_url)

    async def register_metadata(self, image_url: str) -> ImageMetadata:
        raw_image_metadata = await self.inspect_image_metadata(image_url)
        self.logger.debug(f"Image metadata is {raw_image_metadata}")
        metadata = self.__get_metadata(raw_image_metadata)
        self.logger.debug(f"decoded image metadata for image {image_url} is {metadata}")

        digest = raw_image_metadata.get(self.oci_labels_config.DIGEST_KEY)

        if not digest:
            raise HTTPException(status_code=404, detail="digest not found for the image")

        image_metadata = ImageMetadata(
            image_id=image_url,
            name=metadata.get("Name"),
            author_name=metadata.get("Author"),
            types=metadata.get("Types"),
            digest=digest,
            tag=metadata.get("Version")
        )

        await self.image_metadata_repository.register_metadata(image_metadata)
        return image_metadata

    @staticmethod
    def __name_tag_from_image_url(image_url: str) -> (str, str):
        name_with_tag = image_url.split("/")[-1]
        return name_with_tag.split(":")[0], name_with_tag.split(":")[1]

    def __get_metadata(self, raw_image_metadata: dict) -> dict:
        if self.oci_labels_config.ANNOTATION_KEY not in raw_image_metadata:
            self.logger.error("annotations not found for the image")
            raise HTTPException(status_code=404, detail="annotations not found for the image")

        annotations = raw_image_metadata.get(self.oci_labels_config.ANNOTATION_KEY)
        if self.oci_labels_config.METADATA_KEY not in annotations:
            self.logger.error("metadata not found for the image")
            raise HTTPException(status_code=404, detail="metadata not found for the image")

        encoded_metadata = annotations.get(self.oci_labels_config.METADATA_KEY)
        return self.__decode_metadata(encoded_metadata)

    @staticmethod
    def __decode_metadata(encoded_data) -> dict:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        return json.loads(decoded_data)
