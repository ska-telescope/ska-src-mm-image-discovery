from typing import List

from pydantic import BaseModel, Field

from src.ska_src_mm_image_discovery_api.models.software.executable.message_item import MessageItem


class AbstractComponent(BaseModel):
    uuid: str = Field(..., description="The UUID of the component")
    name: str = Field(..., description="The name of the component")
    type: str = Field(..., description="The type of the component")
    created: str = Field(..., description="The date and time the component was created")
    messages: List[MessageItem] = Field(..., description="The message items")
