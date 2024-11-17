from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class Credentils(BaseModel):
    account: Annotated[str, None]
    password: Annotated[str, None]
    
    
    
class User(BaseModel):
    account: Annotated[str, None]
    username: Annotated[str, None]
    
class UserResponse(User):
    pass

class NewUser(User):
    password: Annotated[str, None]
    repassword: Annotated[str, None]
    