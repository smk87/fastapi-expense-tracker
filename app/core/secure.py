from typing import Annotated

from core.db import get_db
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    from core.jwt_helper import verify_access_token
    from models.user import User

    try:
        payload = verify_access_token(token)
        user_id = payload.get("id")
        email = payload.get("email")
        user = db.query(User).filter(User.id == user_id).first()

        if user_id is None or email is None or user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        request.state.user = user

    except Exception as e:
        print("Error in getting user", e)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
