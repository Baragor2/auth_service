from datetime import datetime, UTC, timedelta
from typing import Annotated

import bcrypt
from fastapi import Cookie, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import auth_settings, settings
from app.database import users
from app.exceptions import IncorrectUsernameOrPasswordException, TokenAbsentException, IncorrectTokenFormatException, \
    TokenExpiredException, UserIsNotPresentException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    secret_key = auth_settings.private_key_pass.read_text().encode()
    encoded_jwt = jwt.encode(to_encode, secret_key, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await users.find_one({"email": email})
    check_result = await validate_password(password, user["hashed_password"])
    if not user or not check_result:
        raise IncorrectUsernameOrPasswordException
    return user


async def get_token(token: str) -> Annotated[str, Cookie]:
    # token = request.cookies.get("admin_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str):
    token: str = await get_token(token)

    try:
        secret_key = auth_settings.private_key_pass.read_text().encode()
        payload = jwt.decode(token, secret_key, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise TokenExpiredException

    email: str = payload.get("sub")
    if not email:
        raise UserIsNotPresentException

    user = await users.find_one({"email": email})
    if not user:
        raise UserIsNotPresentException
    return user
