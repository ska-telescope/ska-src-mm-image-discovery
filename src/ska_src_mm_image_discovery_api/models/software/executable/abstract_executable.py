from pydantic import Field

from src.ska_src_mm_image_discovery_api.models.software.executable.abstract_component import AbstractComponent
from src.ska_src_mm_image_discovery_api.models.software.executable.executable_access_list import ExecutableAccessList


class AbstractExecutable(AbstractComponent):
    type: str = Field(..., description="The component type discriminator")
    access : ExecutableAccessList