from typing import Annotated
from pydantic import BaseModel


from .user import User, UserResponse
from .transfer_data import *



class ShellList(BaseModel):
    name: Annotated[str, None]
    shell: Annotated[str, None]