from pydantic import BaseModel , Field


class DockerInternalPort(BaseModel):
    """
    DockerInternalPort represents a port that is internal to the Docker container.
    """
    port: int = Field(..., description="Port number inside the container")


class DockerExternalPort(BaseModel):
    port: int = Field(..., description="Exposed port on the host.")
    addresses: list[str] = Field(..., description="List of hostnames or IP addresses for the external interface.")



class DockerNetworkPort(BaseModel):
    """
    "Details of a network port exposed on the container."
    """
    access: bool = Field(..., description="Flag to indicate if this port is exposed to clients.")
    internal : DockerInternalPort = Field(..., description="Internal port of the container.")
    external : DockerExternalPort = Field(..., description="External port of the container.")
    protocol: str = Field(..., description="Protocol used (e.g., TCP, UDP, HTTP, HTTPS)")
    path: str = Field(..., description="Path segment of the access URL")
