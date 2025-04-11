from typing import Union

from src.ska_src_mm_image_discovery_api.models.software.executable.executableType.docker_container.docker_container import \
    DockerContainer
from src.ska_src_mm_image_discovery_api.models.software.executable.executableType.jupyter_notebook.jupyter_notebook import \
    JupyterNotebook
from src.ska_src_mm_image_discovery_api.models.software.executable.executableType.singularity_container.singularity_container import \
    SingularityContainer
from src.ska_src_mm_image_discovery_api.models.software.resources.simple_compute_memory_spec import \
    SimpleComputeResource

ExecutableUnion = Union[DockerContainer, SingularityContainer, JupyterNotebook]
ResourceUnion = Union[SimpleComputeResource]
