from typing import Annotated, TypeAlias

from annotated_types import MinLen
from pydantic import BaseModel, EmailStr

Password: TypeAlias = Annotated[str, MinLen(8)]


class SUser(BaseModel):
    email: EmailStr
    password: Password


class SUserInsert(BaseModel):
    email: EmailStr
    hashed_password: bytes
