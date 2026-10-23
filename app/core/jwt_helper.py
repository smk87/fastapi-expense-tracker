import os
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from fastapi import HTTPException, status
from jose import jwt

load_dotenv()

access_token_expire_minutes = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
secret_key = os.environ.get("SECRET_KEY", "")
algorithm = os.environ.get("ALGORITHM", "HS256")


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> tuple[str, datetime]:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=access_token_expire_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return encoded_jwt, expire


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        return payload

    except jwt.JWSError:
        print("Invalid token")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
