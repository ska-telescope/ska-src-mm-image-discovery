from typing import Literal, List

from pydantic import BaseModel, Field


class ExecutableAccessMethod(BaseModel):
    status: Literal["PREPARING", "ACTIVE", "FINISHED"]
    protocol: str = Field(..., description="Protocol")
    locations: List[str] = Field(..., min_items=1, description="Locations")
