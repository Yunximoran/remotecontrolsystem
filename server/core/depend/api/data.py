import json
import asyncio
from typing import Annotated

from fastapi import(
    APIRouter,
    WebSocket,
    WebSocketDisconnect
    )

from databasetool import Redis

# 数据接口
router = APIRouter()
prefix = "/server/data"
tags = ["data"]

@router.get("/accounts")
async def get_account_data(account: Annotated[str, None]):
    # 从数据库中获取账号数据，校验账号是否存在
    account_infomation = Redis.hget("accounts", account)
    if account_infomation is not None:
        return json.loads(account_infomation)
    return {'start': "not data"}

@router.get("/realtime")
async def get_realtime_data():
    return {
        "client_status": Redis.hgetall("client_status"),
        "client_reports": Redis.hgetall("reports"),
        "client_waitdones": Redis.hgetall("waitdones"),
        "softwarelist": Redis.lrange("softwarelist"),
        "logs": Redis.lrange("logs")
    }