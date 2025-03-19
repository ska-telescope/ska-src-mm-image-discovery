from typing import List

from pydantic import BaseModel, Field


class Executable(BaseModel):
    name: str
    type: str
    location: str


class Metadata(BaseModel):
    description: str | None
    version: str
    tag: str | None
    authorName: str = Field(..., alias='authorName')  # TODO - change to author_name
    digest: str | None
    specifications: List[str] | None


class ResourceLimit(BaseModel):
    min: int
    max: int


class Resources(BaseModel):
    cores: ResourceLimit
    memory: ResourceLimit


class SoftwareMetadata(BaseModel):
    executable: Executable
    metadata: Metadata
    resources: Resources | None
