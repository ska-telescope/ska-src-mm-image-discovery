from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class MetadataService:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    async def get_all_metadata(self, metadata_filter: dict) -> list[ImageMetadata]:
        metadata_filter = {"types": metadata_filter.get('type_name')} if metadata_filter.get(
            'type_name') is not None else {}
        image_metadata_list = []
        documents = await self.mongo_repository.get_all_metadata(metadata_filter)
        for document in documents:
            image_metadata = ImageMetadata(**document)
            image_metadata_list.append(image_metadata)
        return image_metadata_list

    async def get_metadata_by_image_id(self, image_id: str) -> ImageMetadata:
        document =  await self.mongo_repository.get_metadata_by_image_id(image_id)
        return ImageMetadata(**document)
