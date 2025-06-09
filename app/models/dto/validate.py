from pydantic import BaseModel, Field


class ValidateDTO(BaseModel):
    has_error: bool = Field(default=False, exclude=True)
    error_msg: str = ""
