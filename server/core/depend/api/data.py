import json
import asyncio
from typing import Annotated

from fastapi import(
    APIRouter,
    WebSocket,
    WebSocketDisconnect
    )

from databasetool import DataBaseManager as DATABASE

# 数据接口
router = APIRouter()


@router.websocket("/ws")
async def predict(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            client_status = DATABASE.hgetall("client_status")
            client_reports = DATABASE.hgetall("reports")
            client_waitdones = DATABASE.hgetall("waitdones")
            softwarelist = DATABASE.lrange("softwarelist")
            logs = DATABASE.lrange("logs")
            await websocket.send_json([client_status, client_reports, client_waitdones, softwarelist, logs])
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("链接中断")



@router.get("/accounts", tags=['user'])
async def get_account_data(account: Annotated[str, None]):
    # 从数据库中获取账号数据，校验账号是否存在
    account_infomation = DATABASE.hget("accounts", account)
    if account_infomation is not None:
        return json.loads(account_infomation)
    
    return {'start': "not data"}
