from datetime import datetime

from pydantic import BaseModel, Field
from schemas.user import UserResponseDto


class LoginRequestDto(BaseModel):
    email: str = Field(
        ..., description="The email of the user", examples=["example@gmail.com"]
    )

    password: str = Field(
        ..., description="The password of the user", examples=["password"]
    )


class LoginResponseDto(BaseModel):
    access_token: str = Field(
        ..., description="The access token", examples=["access_token"]
    )
    expires_at: datetime | str = Field(
        ..., description="The expiry time", examples=["2026-10-23T15:24:00Z"]
    )
    user: UserResponseDto = Field(
        ...,
        description="The user",
        examples=[
            UserResponseDto(
                id=1, username="user", email="[EMAIL_ADDRESS]", created_at="2022-01-01"
            )
        ],
    )
    model_config = {"from_attributes": True}
