from enum import Enum
from typing import Literal

from pydantic import Field , BaseModel

from src.ska_src_mm_image_discovery_api.models.software.executable.abstract_component import AbstractComponent
from src.ska_src_mm_image_discovery_api.models.software.executable.abstract_executable import AbstractExecutable
from src.ska_src_mm_image_discovery_api.models.software.resources.abstract_compute_resource import \
    AbstractComputeResource


class Resource(BaseModel):
    min : int
    max : int


class SimpleComputeMemory(BaseModel):
    requested : Resource = Field(..., description="The amount of memory requested by the execution. The minimum represents the lower limit that the execution requires. The maximum represents the highest amount of memory that the execution can use. All values are given in multiples of 'GiB'")
    offered : Resource = Field(..., description="The amount of memory offered by the execution. The minimum represents the lower limit that the execution requires. The maximum represents the highest amount of memory that the execution can use. All values are given in multiples of 'GiB'")


class SimpleComputeCores(BaseModel):
    requested : Resource = Field(..., description="The number of CPU cores requested by the user. The minimum represents the lower limit that the execution requires. The maximum represents the highest number of cores that the execution can use.")
    offered : Resource = Field(..., description="The number of CPU cores offered by the user. The minimum represents the lower limit that the execution requires. The maximum represents the highest number of cores that the execution can use.")

class Mode(str , Enum):
    READONLY : "READONLY"
    READWRITE: "READWRITE"


class SimpleComputeVolume(AbstractComponent):
    path: str = Field(..., description="The mount point in the target filesystem.")
    mode : Mode  = Field(..., description="The read-write mode.")
    resource : str = Field(..., description="The name or UUID of the resource to mount.")

class SimpleComputeSpec(BaseModel):
    cores: SimpleComputeCores = Field(..., description="The CPU cores requested by the execution.")
    memory: SimpleComputeMemory = Field(..., description="The memory requested by the execution.")
    volumes: list[SimpleComputeVolume] = Field(..., description="The volumes requested by the execution.")



class SimpleComputeResource(AbstractComputeResource , SimpleComputeSpec):
    type : Literal["https://www.purl.org/ivoa.net/EB/schema/types/resources/compute/simple-compute-resource-1.0"] = Field(..., description="The component type discriminator")
