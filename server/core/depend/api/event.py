
import re
import json
from typing import Annotated
from fastapi import APIRouter

from lib import Resolver
from datamodel import WaitDesposeResults
from datamodel.transfer_data import Software
from core.depend.control import Control
from gloabl import DB

resolver = Resolver()
controlor = Control()

# 事件接口
router = APIRouter()
prefix = "/server/event"
tags = ["event"]

# 待办事件已处理事件
@router.put("/desposedsoftware")
async def despose_waitdones(res: WaitDesposeResults):
    print("despose waitdone api data:", res.cookie, res.results)
    # 将待办实现处理结果保存redis
    DB.hset("waitdone_despose_results", res.cookie, res.results)

# 激活客户端
@router.put("/wol")
async def magic_client(toclients:Annotated[list, None] = []):
    """
        发送唤醒魔术包
    toclients: 指定发送目标IP
    """
    try:
        controlor.sendtoclient(toclients, wol=True)
    except Exception:
        return {"ERROR", "wol err"}
    

# ========= 默认事件========== #
# 添加软件清单
@router.put("/addsoftwarelist")
async def addsoftwarelist(software: Software):
    """
        let data = {
            software: {
                ecdis: {
                    "name": "XXX",
                    "path": "xxx"
                },
                "conning": false
            }
        }
    """
    info = software.model_dump_json()
    
    # 移除就得软件信息
    for i, sf in enumerate(DB.lrange("softwarelist")):
        item = json.loads(sf)
        if item['ecdis']["name"] == software.ecdis.name:
            DB.lpop("softwarelist", i)
            
    DB.lpush("softwarelist", info)
    return {"OK", software.ecdis.name}

@router.put("/popsoftwarelist")
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


    


