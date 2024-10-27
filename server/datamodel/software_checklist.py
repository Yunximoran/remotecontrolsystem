# 软件清单数据模型
from typing import Annotated
from pydantic import BaseModel


class SoftWare(BaseModel):
    name: Annotated[str, None]  
    start: Annotated[str, None] = None

class SoftWareCheckList(BaseModel):
    software: list[SoftWare]
    
