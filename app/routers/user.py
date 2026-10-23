from typing import Annotated

from core.db import get_db
from core.password_hasher import hash_password
from core.secure import get_current_user
from fastapi import APIRouter, Depends, Response, status
from models.user import User
from schemas.api_response import APIResponse
from schemas.user import UserCreateDto, UserResponseDto, UserUpdateDto
from sqlalchemy import or_
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=APIResponse[UserResponseDto])
def create_user(
    payload: UserCreateDto, db: Annotated[Session, Depends(get_db)], response: Response
):
    db_user = (
        db.query(User)
        .filter(or_(User.username == payload.username, User.email == payload.email))
        .first()
    )

    if db_user:
        response.status_code = status.HTTP_400_BAD_REQUEST

        return APIResponse[UserResponseDto](
            status="failed", message="Username or email already in use"
        )

    new_user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return APIResponse[UserResponseDto](
        status="success",
        message="User created successfully",
        data=new_user,
    )


@user_router.get("/", response_model=APIResponse[list[UserResponseDto]])
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    users = db.query(User).all()

    return APIResponse[list[UserResponseDto]](
        status="success", message="Users fetched successfully", data=users
    )


@user_router.get("/{id}", response_model=APIResponse[UserResponseDto])
def get_user_by_id(
    id: str,
    db: Annotated[Session, Depends(get_db)],
    response: Response,
    user: Annotated[User, Depends(get_current_user)],
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND

        return APIResponse[UserResponseDto](
            status="failed",
            message="User not found",
        )

    return APIResponse[UserResponseDto](
        status="success", message="User fetched successfully", data=user
    )


@user_router.put("/{id}", response_model=APIResponse[UserResponseDto])
def update_user(
    id: str,
    payload: UserUpdateDto,
    db: Annotated[Session, Depends(get_db)],
    response: Response,
    user: Annotated[User, Depends(get_current_user)],
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND

        return APIResponse[UserResponseDto](
            status="failed",
            message="User not found",
        )

    if payload.username is not None:
        user.username = payload.username

    if payload.email is not None:
        user.email = payload.email

    if payload.password is not None:
        user.password = hash_password(payload.password)

    db.commit()
    db.refresh(user)

    return APIResponse[UserResponseDto](
        status="success", message="User updated successfully", data=user
    )


@user_router.delete("/{id}", response_model=APIResponse[None])
def delete_user(
    id: str,
    db: Annotated[Session, Depends(get_db)],
    response: Response,
    user: Annotated[User, Depends(get_current_user)],
):
    user = db.get(User, id)

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND

        return APIResponse[UserResponseDto](
            status="failed",
            message="User not found",
        )

    db.delete(user)
    db.commit()

    return APIResponse[UserResponseDto](
        status="success", message="User deleted successfully"
    )
