from typing import Annotated

from core.db import get_db
from core.jwt_helper import create_access_token
from core.password_hasher import verify_password
from fastapi import APIRouter, Depends, Response, status
from models.user import User
from schemas.api_response import APIResponse
from schemas.auth import LoginRequestDto, LoginResponseDto
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
def login_user(
    payload: LoginRequestDto,
    db: Annotated[Session, Depends(get_db)],
    response: Response,
):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED

        return APIResponse[None](status="failed", message="Invalid email or password")

    is_valid_password = verify_password(payload.password, user.password)

    if not is_valid_password:
        response.status_code = status.HTTP_401_UNAUTHORIZED

        return APIResponse[None](status="failed", message="Invalid email or password")

    [access_token, expires_at] = create_access_token(
        {"id": user.id, "email": user.email, "username": user.username}
    )

    return APIResponse[LoginResponseDto](
        status="success",
        message="Login successful",
        data=LoginResponseDto(
            access_token=access_token, expires_at=expires_at, user=user
        ),
    )
