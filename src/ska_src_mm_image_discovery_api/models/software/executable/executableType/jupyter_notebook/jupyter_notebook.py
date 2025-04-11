from typing import Literal

from pydantic import BaseModel, Field

from src.ska_src_mm_image_discovery_api.models.software.executable.abstract_executable import AbstractExecutable


class JupyterNotebookSpec(BaseModel):
    location: str = Field(..., title="The URL of the notebook.")

class JupyterNotebook(AbstractExecutable , JupyterNotebookSpec):
    type: Literal["https://www.purl.org/ivoa.net/EB/schema/types/executables/jupyter-notebook-1.0"] = Field(...,description="The component type discriminator")