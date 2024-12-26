from typing import Annotated, Union, List, Dict, Any
from pydantic import BaseModel


from .user import User, UserResponse, NewUser, Credentils
from .transfer_data import *



class ShellList(BaseModel):
    name: Annotated[str, None]
    shell: Annotated[str, None]
    

class WaitDesposeResults(BaseModel):
    cookie: Annotated[float, None]
    results: Annotated[str, None]