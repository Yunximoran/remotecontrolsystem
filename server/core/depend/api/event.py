
import re
import json
from typing import Annotated
from fastapi import APIRouter

from projectdesposetool import choose_file
from databasetool import Redis
from datamodel import WaitDesposeResults
from datamodel import Software
from core.depend.control import Control

controlor = Control()

# 事件接口
router = APIRouter()
prefix = "/server/event"
tags = ["event"]

# 待办事件已处理事件
@router.put("/desposedsoftware")
async def despose_waitdones(res: WaitDesposeResults):
    print("despose waitdone api data:", res.cookie, res.results)
    Redis.hset("waitdone_despose_results", res.cookie, res.results)

# 激活客户端
@router.put("/wol")
async def magic_client(toclients:Annotated[list, None] = []):
    controlor.sendwol_allclient(toclients)

# ========= 默认事件========== #
# 添加软件清单
@router.put("/addsoftwarelist")
async def addsoftwarelist(
        softwarename: Annotated[str, None], 
        version: Annotated[str, None] = None
    ):
    """
   softwarename: 软件名称
   version: 软件版本[可选]
    """
    executablefile, softwarepath = choose_file()
    software = {
        "ecdis": {
            "name": softwarename,
            "executable": executablefile,
            "path": softwarepath,
            "version": version
        },
        "conning": False
    }
    Redis.lpush("softwarelist", json.dumps(software))
    return {"OK", softwarename}

# 移除软件清单
@router.put("/popsoftwarelist")
async def popsoftwarelist(software):
    softwarelist = Redis.lrange("softwarelist")
    for i, item in enumerate(softwarelist):
        if re.match(software, item):
            Redis.lpop("softwarelist", i)

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
    filename, filepath = choose_file()
    with open(filepath, "rb") as f:
        controlor.sendtoclient(toclients, files=[filename, f])

    


