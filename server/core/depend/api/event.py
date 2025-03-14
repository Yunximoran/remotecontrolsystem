
import re
import json
from typing import Annotated
from fastapi import APIRouter

from lib import Resolver
from lib.ui.explorer import choose_file
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
    controlor.sendtoclient(toclients, wol=True)

# ========= 默认事件========== #
# 添加软件清单
@router.put("/addsoftwarelist")
async def addsoftwarelist(software: Software):
    """
        software model
    """
    info = software.model_dump_json()
    DB.lpush("softwarelist", info)
    return {"OK", info["ecdis"]["name"]}
    # # 打开资源管理器，选择添加软件
    # executablefile, softwarepath = choose_file()
    # software = {
    #     "ecdis": {
    #         "name": softwarename,
    #         "executable": executablefile,
    #         "path": softwarepath,
    #         "version": version
    #     },
    #     "conning": False
    # }
    # DB.lpush("softwarelist", json.dumps(software))
    # return {"OK", softwarename}

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

# 下载文件
@router.put("/download")
async def download(toclients=[]):
    """
    toclients: 指定向哪些客户端发送数据【默认向所有连接中的客户端发送数据】
    
        从服务端下载文件
    打开资源管理器
    查找需要下载至客户端的文件
    发送文件至客户端
    """
    # 打开资源管理器， 选择下载文件
    filename, filepath = choose_file()
    with open(filepath, "rb") as f:
        # 二进制打开文件
        controlor.sendtoclient(toclients, files=[filename, f])

    


