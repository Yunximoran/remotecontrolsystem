# 心跳包数据模型

from typing import Annotated

from fastapi import Query
from pydantic import BaseModel
from .software import Software

    
class HeartPkgs(BaseModel):
    mac: Annotated[str, None] = \
        Query(pattern="([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
    ip: Annotated[str, None] = \
        Query(pattern="((1\d{2}\.)|(2[0-5]{2}\.)|(\d{1,2}\.)){3}((1\d{2}\.)|(\d{3}\.))")
    software: Annotated[Software, None] = None
    
