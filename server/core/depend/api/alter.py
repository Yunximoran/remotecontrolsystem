# alter 修改一些配置选项

from fastapi import APIRouter
from lib import Resolver
from gloabl import DB

resolver = Resolver()
# 接口信息
router = APIRouter()
prefix = "/server/alter"
tags = ["alter"]

@router.put('/alias')
async def setalias(alias, ip):
    DB.hset("ip_alias", alias, ip)      # 需要暴露
    return {"OK": f"set alias: {alias} -> {ip}"}