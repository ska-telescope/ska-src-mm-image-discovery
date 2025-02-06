from pydantic import BaseModel


class ImageMetadata(BaseModel):
    image_id: str
    author_name: str
    types: list[str]
    digest: str
    tag: str
