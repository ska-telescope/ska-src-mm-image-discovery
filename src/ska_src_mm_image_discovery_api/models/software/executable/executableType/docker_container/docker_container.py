from typing import Literal

from pydantic import BaseModel, Field

from src.ska_src_mm_image_discovery_api.models.software.executable.abstract_executable import AbstractExecutable
from src.ska_src_mm_image_discovery_api.models.software.executable.executableType.docker_container.docker_network_port import \
    DockerNetworkPort
from src.ska_src_mm_image_discovery_api.models.software.executable.executableType.docker_container.docker_spec import \
    DockerImageSpec


class DockerContainerSpec(BaseModel):
    image: DockerImageSpec = Field(..., description="Details of the container image.")
    privileged: bool = Field(default=False, description="Set the privileged flag on execution. The default is `false`.")
    entrypoint: str = Field(..., description="Overwrite the default ENTRYPOINT of the image")
    network: DockerNetworkPort = Field(..., description="Details of the network access available to the container")


class DockerContainer(AbstractExecutable , DockerContainerSpec):
    type : Literal["https://www.purl.org/ivoa.net/EB/schema/types/executables/docker-container-1.0"] = Field(..., description="The component type discriminator")
