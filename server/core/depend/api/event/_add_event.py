
import json
from typing import Set
from fastapi import APIRouter

from lib import Resolver
from datamodel import Classify
from datamodel.transfer_data import Software
from core.depend.control import Control
from gloabl import DB

resolver = Resolver()
controlor = Control()

# 事件接口
router = APIRouter()
prefix = "/server/event/add"
tags = ["add"]


# ========= 添加事件 ========== #
@router.put("/softwarelist")    # 添加软件清单
async def addsoftwarelist(software: Software):
    """
        添加软件清单
    """
    info = software.model_dump_json()
    DB.hset("softwarelist", software.ecdis.name, info)
    return {"OK", software.ecdis.name}
    
@router.put("/add/classify")
async def addclissify(classify: Classify):
    # 检查分类是否存在，否则新建分类
    classifylist = DB.smembers("classifylist")
    if classify.name not in classifylist:
        DB.sadd("classifylist", classify.name)
    
    # 检查ips是否为空，否则只创建分类
    if classify.items is {}:
        return {"OK": f"created classify: {classify.name}"}
    
    
    items = {item.model_dump_json() for item in classify.items}
    # 转化集合， 防止重复ip
    clndata = DB.hget("classify", classify.name)
    
    # 检查当前分类是否为空
    if clndata:
        clndata = set(json.loads(clndata))
        clndata = list(clndata | items)
    else:
        clndata = list(items)
    # # 更新数据
    DB.hset("classify", classify.name, json.dumps(clndata, ensure_ascii=False))
    return {"OK": f"update: {clndata}"}
