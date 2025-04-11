from pydantic import BaseModel, Field


class MessageItem(BaseModel):
    type: str = Field(..., description="The message type uri")
    time: str = Field(..., description="The message time")
    level: str = Field(..., description="The severity level (e.g., INFO, ERROR, etc.)")
    template: str = Field(..., description="The message template")
    values: dict[str, str] = Field(..., description="Key value pairs for the message template")
    message: str = Field(..., description="The message text")
