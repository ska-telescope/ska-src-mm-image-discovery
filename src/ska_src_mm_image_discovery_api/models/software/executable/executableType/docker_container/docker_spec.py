from pydantic import BaseModel, Field

from src.ska_src_mm_image_discovery_api.models.software.executable.executableType.docker_container.docker_network_port import \
    DockerNetworkPort


class DockerPlatformSpec(BaseModel):
    architecture: str = Field(default="amd64" ,description="The CPU architecture the image is built for. Default is amd64.")
    os: str = Field(default="Linux" , description="The OS the image is built for. Default is linux.")

class DockerImageSpec(BaseModel):
    locations : list[str] = Field(..., min_items=1, description="An array of repository locations.")
    digest: str = Field(..., description="Content-addressable image digest generated as a sha256 checksum.")
    platform: DockerPlatformSpec = Field(..., description="Details of the platform the container image is built for.")

class DockerNetworkSpec(BaseModel):
    ports:list[DockerNetworkPort] = Field(..., description="An array of network ports to publish.")