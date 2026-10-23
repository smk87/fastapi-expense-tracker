from datetime import datetime

from pydantic import BaseModel, Field


class UserCreateDto(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=20)


class UserUpdateDto(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=100)
    email: str | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=8, max_length=20)


class UserResponseDto(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime | str

    model_config = {"from_attributes": True}
