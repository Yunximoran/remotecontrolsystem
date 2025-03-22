from typing import Annotated, List

from fastapi import APIRouter

from ._add_event import router as addevent
from ._pop_event import router as popevent

from core.depend.control import Control
from datamodel import WaitDesposeResults
from gloabl import DB

controlor = Control()
router = APIRouter()
prefix="/server/event"
tags = ["event"]

router.include_router(addevent)
router.include_router(popevent)


# 激活客户端
@router.put("/wol")
async def magic_client(toclients:Annotated[List, None] = []):
    """
        发送唤醒魔术包
    toclients: 指定发送目标IP
    """
    try:
        controlor.sendtoclient(toclients, wol=True)
    except Exception:
        return {"ERROR", "wol err"}

# 待办事件已处理事件
@router.put("/desposedsoftware")
async def despose_waitdones(res: WaitDesposeResults):
    # 将待办实现处理结果保存redis
    DB.hset("waitdone_despose_results", res.cookie, res.results)
    return {"OK": f"disposed: {res.cookie}"}