from typing import List
from pydantic import BaseModel

from src.ska_src_mm_image_discovery_api.models.software.executable.executable_access_method import \
    ExecutableAccessMethod


class ExecutableAccessList(BaseModel):
    __root__ : List[ExecutableAccessMethod]
