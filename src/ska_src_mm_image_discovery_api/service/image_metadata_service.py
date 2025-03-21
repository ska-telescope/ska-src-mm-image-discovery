import base64
import json
import logging

from fastapi import HTTPException

from src.ska_src_mm_image_discovery_api.common.skopeo import Skopeo
from src.ska_src_mm_image_discovery_api.config.oci_config import OciConfig
from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.models.software_metadata import SoftwareMetadata, Executable, Metadata, \
    Resources
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class ImageMetadataService:
    logger = logging.getLogger("uvicorn")

    def __init__(self, oci_labels_config: OciConfig, mongo_repository: MongoRepository, skopeo: Skopeo):
        self.oci_labels_config = oci_labels_config
        self.mongo_repository = mongo_repository
        self.skopeo = skopeo

    # todo: should accept empty metadata filter
    async def get_all_image_metadata(self, metadata_filter: dict) -> list[ImageMetadata]:
        documents = await self.mongo_repository.get_all_image_metadata(metadata_filter['type_name'])
        image_metadata_list = []

        for metadata in documents:
            image_executable = metadata.get('executable')
            image_metadata = metadata.get('metadata')

            image_metadata_list.append(ImageMetadata(
                image_id=image_executable.get('location'),
                name=image_executable.get('name'),
                author_name=image_metadata.get("authorName"),
                types=image_metadata.get("specifications"),
                digest=image_metadata.get("digest"),
                tag=image_metadata.get("tag")
            ))

        return image_metadata_list

    async def get_image_metadata_by_image_location(self, image_location: str) -> ImageMetadata:
        metadata = await self.mongo_repository.get_image_metadata_by_location(image_location)

        if metadata is None:
            self.logger.error(f"Image with id {image_location} not found")
            raise HTTPException(status_code=404, detail=f"Image with id {image_location} not found")

        image_executable = metadata.get('executable')
        image_metadata = metadata.get('metadata')

        return ImageMetadata(
            image_id=image_executable.get('location'),
            name=image_executable.get('name'),
            author_name=image_metadata.get("authorName"),
            types=image_metadata.get("specifications"),
            digest=image_metadata.get("digest"),
            tag=image_metadata.get("tag")
        )

    async def inspect_image_metadata(self, image_url: str) -> dict:
        return await self.skopeo.inspect(image_url)

    async def register_metadata(self, image_url: str) -> ImageMetadata:
        raw_image_metadata = await self.inspect_image_metadata(image_url)
        self.logger.debug(f"Image metadata is {raw_image_metadata}")
        metadata = self.__get_metadata(raw_image_metadata)
        self.logger.debug(f"decoded image metadata is {metadata}")
        (image_name, tag) = self.__name_tag_from_image_url(image_url)
        image_name = metadata.get("Name", image_name)
        self.logger.debug(f"Image name is {image_name}, tag is {tag}")

        software_metadata = SoftwareMetadata(
            executable=Executable(name=image_name, type="docker-container", location=image_url),
            metadata=Metadata(description=f"This is a docker container with name {image_name}",
                              version=metadata.get("Version"),
                              tag=tag,
                              authorName=metadata.get("Author"),
                              digest=raw_image_metadata.get(self.oci_labels_config.DIGEST_KEY),
                              specifications=metadata.get("Types")),
            resources=Resources(**self.oci_labels_config.DEFAULT_OCI_RESOURCE)
        )

        await self.mongo_repository.add_software_metadata("docker-container", software_metadata)

        image_metadata = ImageMetadata(
            image_id=image_url,
            name=image_name,
            author_name=metadata.get("Author"),
            types=metadata.get("Types"),
            digest=raw_image_metadata.get(self.oci_labels_config.DIGEST_KEY),
            tag=metadata.get("Version")
        )
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
