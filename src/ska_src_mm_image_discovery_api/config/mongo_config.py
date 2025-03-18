from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class MongoConfig:

    def __init__(self, uri: str, metadata_db: str, metadata_collections: dict):
        self.uri = uri
        self.metadata_db = metadata_db
        self.__metadata_collections = metadata_collections

    @property
    def URI(self) -> str:
        return self.uri

    @property
    def DB(self) -> str:
        return self.metadata_db

    @property
    def Collection(self) -> str:
        return self.__metadata_collections["images"]
