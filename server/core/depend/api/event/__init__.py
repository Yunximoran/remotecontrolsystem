from typing import Annotated, List

from fastapi import APIRouter

from core.depend.control import Control
from datamodel import WaitDesposeResults
from static import DB


from . import _add_event as add
from . import _pop_event as pop

controlor = Control()
router = APIRouter()
prefix="/server/event"
tags = ["event"]

router.include_router(
    router=add.router,
    prefix=add.prefix,
    tags=add.tags
)
router.include_router(
    router=pop.router,
    prefix=pop.prefix,
    tags=pop.tags
)


# 激活客户端
@router.put("/wol")
async def magic_client(toclients:Annotated[List, None] = []):
    """
        发送唤醒魔术包
    toclients: 指定发送目标IP
    """
    try:
        print("WOL")
        controlor.sendtoclient(toclients, wol=True)
    except Exception:
        print("WOL ERROR")
        return {"ERROR", "wol err"}

# 待办事件已处理事件
@router.put("/desposedsoftware")
async def despose_waitdones(res: WaitDesposeResults):
    # 将待办实现处理结果保存redis
    DB.hset("waitdone_despose_results", res.cookie, res.results)
    return {"OK": f"disposed: {res.cookie}"}