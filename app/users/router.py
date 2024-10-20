from typing import Annotated

from fastapi import APIRouter, status, Response, Body, Request
from pymongo.errors import DuplicateKeyError

from app.database import users, admin_password
from app.exceptions import UserAlreadyExistsException, IncorrectUsernameOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token, validate_password, \
    get_current_user
from app.users.schemas import SUser, SUserInsert

router = APIRouter(
     prefix="/users",
     tags=["Users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        user_data: SUser,
        admin_password_to_check: Annotated[str, Body()]
) -> dict[str, str]:
    admin_hashed_pass = await admin_password.find_one({"unique_id": 1})
    if not await validate_password(admin_password_to_check, admin_hashed_pass["admin_password"]):
        raise IncorrectUsernameOrPasswordException

    try:
        hashed_password = await get_password_hash(user_data.password)
        user_to_insert = SUserInsert(
            email=user_data.email,
            hashed_password=hashed_password,
        )
        await users.insert_one(
            user_to_insert.model_dump(by_alias=True)
        )
    except DuplicateKeyError:
        raise UserAlreadyExistsException
    return {"message": "successful registration"}


@router.post("/login")
async def login_user(
        user_data: SUser,
        admin_password_to_check: Annotated[str, Body()],
        response: Response
) -> dict:
    admin_hashed_pass = await admin_password.find_one({"unique_id": 1})
    if not await validate_password(admin_password_to_check, admin_hashed_pass["admin_password"]):
        raise IncorrectUsernameOrPasswordException

    user = await authenticate_user(user_data.email, user_data.password)
    access_token = await create_access_token({"sub": user["email"]})
    response.set_cookie("admin_access_token", access_token, httponly=True)
    return {"message": "successful login"}


@router.post("/logout")
async def logout_user(response: Response, request: Request) -> dict:
    await get_current_user(request)
    response.delete_cookie("admin_access_token")
    return {"message": "successful logout"}
