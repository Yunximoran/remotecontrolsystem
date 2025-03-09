from typing import Annotated, List, Dict
from fastapi import Query

from pydantic import BaseModel

class Instruct(BaseModel):
    type: Annotated[str, None]
    shell: Annotated[str, None]
    isadmin: Annotated[bool, None] = False
    os: Annotated[str, None] = Query(pattern="^(Windows)$|^(Linux)$|^(MacOS)$", default="Windows")
    kwargs: Annotated[Dict, None] = {}
    
class InstructList(BaseModel):
    items: List[Instruct]
    # N = Annotated[str, None]
    
    
TYPE = {
    "linux": [],
    "windows": []
}


if __name__ == "__main__":
    InstructList.items