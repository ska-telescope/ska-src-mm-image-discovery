import base64
import json
import logging

from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.common.skopeo import Skopeo
from src.ska_src_mm_image_discovery_api.config.oci_labels_config import OciLabelsConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class ImageMetadataService:
    logger = logging.getLogger("uvicorn")

    def __init__(self, oci_labels_config: OciLabelsConfig, mongo_repository: MongoRepository, skopeo: Skopeo):
        self.oci_labels_config = oci_labels_config
        self.mongo_repository = mongo_repository
        self.skopeo = skopeo


    async def get_all_image_metadata(self, metadata_filter: dict) -> list[ImageMetadata]:
        metadata_filter = {"types": metadata_filter.get('type_name')} if metadata_filter.get(
            'type_name') is not None else {}
        image_metadata_list = []
        documents = await self.mongo_repository.get_all_image_metadata(metadata_filter)
        for document in documents:
            image_metadata = ImageMetadata(**document)
            image_metadata_list.append(image_metadata)
        return image_metadata_list

    async def get_image_metadata_by_image_id(self, image_id: str) -> ImageMetadata:
        document = await self.mongo_repository.get_image_metadata_by_image_id(image_id)
        if document is None:
            self.logger.error(f"Image with id {image_id} not found")
            raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found")
        return ImageMetadata(**document)

    async def inspect_image_metadata(self, image_url: str) -> dict:
        return await self.skopeo.inspect(image_url)

    async def register_metadata(self, image_url: str) -> ImageMetadata:
        raw_image_metadata = await self.inspect_image_metadata(image_url)
        self.logger.debug(f"Image metadata found for image {image_url} is {raw_image_metadata}")
        metadata = self.__get_metadata(raw_image_metadata)
        self.logger.debug(f"decoded image metadata found for image {image_url} is {metadata}")

        image_metadata = ImageMetadata(
            image_id=image_url,
            name=metadata.get("Name"),
            author_name=metadata.get("Author"),
            types=metadata.get("Types"),
            digest=raw_image_metadata.get(self.oci_labels_config.DIGEST, "DEFAULT_DIGEST"),
            tag=metadata.get("Version")
        )
        return await self.mongo_repository.register_image_metadata(image_metadata)

    def __get_metadata(self, raw_image_metadata: dict) -> dict:
        if self.oci_labels_config.ANNOTATION not in raw_image_metadata:
            self.logger.error("annotations not found for the image")
            raise HTTPException(status_code=404, detail="annotations not found for the image")

        annotations = raw_image_metadata.get(self.oci_labels_config.ANNOTATION)
        if self.oci_labels_config.METADATA not in annotations:
            self.logger.error("metadata not found for the image")
            raise HTTPException(status_code=404, detail="metadata not found for the image")

        encoded_metadata = annotations.get(self.oci_labels_config.METADATA)
        return self.__decode_metadata(encoded_metadata)


    @staticmethod
    def __decode_metadata(encoded_data) -> dict:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        return json.loads(decoded_data)
