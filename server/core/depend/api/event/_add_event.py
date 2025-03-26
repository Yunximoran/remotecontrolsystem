
import json
import re
from typing import Annotated, List, Set
from fastapi import APIRouter

from lib import Resolver
from lib.math import decimal_to_baseX, baseX_to_decimal
from datamodel import Classify
from datamodel.transfer_data import Software
from datamodel.instruct import Instruct, InstructList
from core.depend.control import Control
from static import DB

resolver = Resolver()
controlor = Control()

# 事件接口
router = APIRouter()
prefix = "/add"
tags = ["add"]

    

# ========= 添加事件 ========== #
@router.put("/softwarelist")    # 添加软件清单
async def addsoftwarelist(software: Annotated[Software, None]):
    """
        添加软件清单
    """
    info = software.model_dump_json()
    DB.hset("softwarelist", software.ecdis.name, info)
    return {"OK", software.ecdis.name}
    
@router.put("/classify")
async def addclissify(classify: Annotated[Classify, None]):
    # 检查分类是否存在，否则新建分类
    # return classify.items
    # classify.items: 不重复列表
    classifylist = DB.smembers("classifylist")
    if classify.name not in classifylist:
        DB.sadd("classifylist", classify.name)
            
    # 检查ips是否为空，否则只创建分类
    if classify.items is {}:
        return {"OK": f"created classify: {classify.name}"}

    # counts = {}
    # items: Set[str] = set()
    # for item in classify.items:
    #     # # 检查引用计数
    #     # count = DB.hget("classified", item.ip)
    #     # # 设置初次引用的值为0， 每次引用 计数器加1
    #     # DB.hset("classified", item.ip, int(count) + 1) if count else DB.hset("classified", item.ip, 0)
    #     if item.ip in counts:
    #         counts[item.ip] += 1
    #     else:
    #         counts[item.ip] = 0
    #     # 另存为集合，防止重复值
    #     items.add(item.model_dump_json())
        
    items = set([item.model_dump_json() for item in classify.items])
    context = DB.hget("classify", classify.name)
    # 检查当前分类是否为空
    if context:
        clndata = set(json.loads(context))  # 解析json， 并转化为集合
        clndata = list(clndata | items)     # 合并两个集合，转化类列表
    else:
        clndata = list(items)
    
    # 更新引用计数
    count = {}   
    for data in clndata:
        item = json.loads(data)
        ip = item['ip']
        if ip in count:
            count[ip] +=1 
        else:
            count[ip] = 0
    
    for ip in count:
        DB.hset("classified", ip, count[ip])
        
    # 更新数据
    DB.hset("classify", classify.name, json.dumps(clndata, ensure_ascii=False))
    return {"OK": f"update: {clndata}"}


@router.put("/set_of_prestored_instructions")
async def add_instructions(alias: Annotated[str, None], instructlist: Annotated[InstructList, None]):
    context = instructlist.model_dump_json()
    DB.hset("instructlist", alias, context)
    return {"OK": f"add prestored instruct: {alias} -> {context}"}