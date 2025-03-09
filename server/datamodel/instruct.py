from typing import Annotated, List

from pydantic import BaseModel

class Instruct(BaseModel):
    type: Annotated[str, None]
    shell: Annotated[str, None]
    
class InstructList(BaseModel):
    items: List[Instruct]

    
    
TYPE = {
    "linux": [],
    "windows": []
}


if __name__ == "__main__":
    InstructList.items