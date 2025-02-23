from typing import Annotated

from pydantic import BaseModel


class Instruct(BaseModel):
    type: Annotated[str, None]
    shell: Annotated[str, None]
    
    
TYPE = {
    "linux": [],
    "windows": []
}