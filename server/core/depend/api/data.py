import json
from typing import Annotated

from fastapi import(
    APIRouter,
    )

from gloabl import DB
from lib import Resolver


resolver = Resolver()

# 数据接口
router = APIRouter()
prefix = "/server/data"
tags = ["data"]

@router.get("/accounts")
async def get_account_data(account: Annotated[str, None]):
    # 从数据库中获取账号数据，校验账号是否存在
    account_infomation = DB.hget("accounts", account)
    if account_infomation is not None:
        return json.loads(account_infomation)
    return {'start': "not data"}

@router.get("/realtime")
async def get_realtime_data():
    """
    实时更新数据，需要定期调用
        从redis中获取数据
    """
    return {"data":{
        "client_status": DB.hgetall("client_status"),
        "client_reports": DB.hgetall("reports"),
        "client_waitdones": DB.hgetall("waitdones"),
    }}