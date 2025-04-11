from typing import Literal

from pydantic import Field
from pydantic.main import BaseModel

from src.ska_src_mm_image_discovery_api.models.software.executable.abstract_executable import AbstractExecutable


class SingularityContainerSpec(BaseModel):
    location : str = Field(..., title="The URL to download the container image from.")

class SingularityContainer(AbstractExecutable, SingularityContainerSpec):
    type: Literal["https://www.purl.org/ivoa.net/EB/schema/types/executables/singularity-container-1.0"] = Field(..., description="The component type discriminator")
