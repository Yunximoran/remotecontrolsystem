# ===== 通信模型 ===== #

from typing import Annotated

from fastapi import Query
from pydantic import BaseModel
from pathlib import Path

# 软件模型
class Ecdis(BaseModel):
    """
        软件状态
    """
    name: Annotated[str, None]
    path:Annotated[Path, None] = None
    

class Software(BaseModel):
    """
        软件模型
    ecdis：心电图， 软件参数
    conning：软件状态
    """
    ecdis: Annotated[Ecdis, None]
    conning: Annotated[bool, None] = False
    
class SoftwareList(BaseModel):
    """
        软件清单
    """
    items: list[Software]
    


# 心跳包模型
class HeartPkgs(BaseModel):
    mac: Annotated[str, None] = \
        Query(pattern="([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
    ip: Annotated[str, None] = \
        Query(pattern="((1\d{2}\.)|(2[0-5]{2}\.)|(\d{1,2}\.)){3}((1\d{2}\.)|(\d{3}\.))")
    softwares: Annotated[SoftwareList, None] = None
    
