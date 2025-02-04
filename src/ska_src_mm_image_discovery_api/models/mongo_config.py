from src.ska_src_mm_image_discovery_api.decorators.singleton import singleton


@singleton
class MongoConfig:

    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name

    @property
    def URI(self) -> str:
        return self.uri

    @property
    def DB(self) -> str:
        return self.db_name

    @property
    def Collection(self) -> str:
        return self.collection_name
