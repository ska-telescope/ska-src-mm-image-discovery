from pydantic import BaseModel


class ImageMetadata(BaseModel):
    image_id: str
    name: str | None ## TODO - change to Fix this None
    author_name: str
    types: list[str]
    digest: str
    tag: str
