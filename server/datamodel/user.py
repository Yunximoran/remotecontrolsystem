from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class User(BaseModel):
    username: Annotated[str, None]
    password: Annotated[str, None]

class UserResponse(BaseModel):
    username: Annotated[str, None]


class NewUser(BaseModel):
    username: Annotated[str, None]
    password: Annotated[str, None]
    repassword: Annotated[str, None]
    