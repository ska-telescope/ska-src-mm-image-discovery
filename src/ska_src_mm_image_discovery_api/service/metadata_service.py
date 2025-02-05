from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton
from src.ska_src_mm_image_discovery_api.models.image_metadata import ImageMetadata
from src.ska_src_mm_image_discovery_api.repository.mongo_repository import MongoRepository


@singleton
class MetadataService:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    async def get_all_metadata(self):
        image_metadata_list = []
        documents = await self.mongo_repository.get_all_metadata()
        for document in documents:
            image_metadata = ImageMetadata(
                image_id=document['image_id'],
                author_name=document['author_name'],
                types=document['types'],
                tag=document['tag'],
                digest=document['digest']
            )
            image_metadata_list.append(image_metadata.to_dict())
        return image_metadata_list
