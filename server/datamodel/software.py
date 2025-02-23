from typing import Annotated

from pydantic import BaseModel

class _Ecdis(BaseModel):
    name: Annotated[str, None]
    version: Annotated[str, None] = "0.0.0"
    path: Annotated[str, None]
    
    
class Software(BaseModel):
    ecdis: Annotated[_Ecdis, None]
    conning: Annotated[bool, None] = False
    
    

