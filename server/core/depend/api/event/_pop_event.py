
import re
import json
from typing import Annotated, List, AnyStr
from fastapi import APIRouter

from lib import Resolver
from datamodel.classify import ClassTable
from datamodel.transfer_data import Software
from core.depend.control import Control
from gloabl import DB

resolver = Resolver()
controlor = Control()

# 事件接口
router = APIRouter()
prefix = "/server/event/pop"
tags = ["pop event"]


# ========= 移除事件 ========== #
@router.put("/pop/softwarelist")
async def popsoftwarelist(software):
    """
        # 移除软件清单
    software: 软件名    
    """
    # 获取当前软件清单
    softwarelist = DB.lrange("softwarelist")
    
    # 找到对应软件
    for i, item in enumerate(softwarelist):
        if re.match(software, item):
            # 删除修改redis表格
            DB.lpop("softwarelist", i)
    return {"OK", f"POP {software}"}


@router.put("/pop/clissify")
async def popclassify(cln, key):
    # 检查分类是否存在
    classifylist = DB.smembers("classifylist")
    if not cln in classifylist:
        return {"ERROR": f"classify: {cln} not exists"}
    
    
    # 读取分类数据
    clndata: List = json.loads(DB.hget("clissify", cln))
    for i, item in enumerate(clndata):
        # 遍历数据表
        if key in (item['soft'], item['ip']):
           obj = clndata.pop(i) 
           DB.hset("classify", cln, json.dumps(clndata, ensure_ascii=False))
           return {"OK": f"remove {obj} form classify: {cln}"}

    return {"ERROR": f"ip not in classify: {cln}"}
    


    


