from typing import Annotated
import re

from fastapi import APIRouter

from projectdesposetool import choose_file
from databasetool import DataBaseManager as DATABASE
from datamodel import WaitDesposeResults
from core.depend.control import Control

controlor = Control()

# 事件接口
router = APIRouter()
prefix = "/server/event"
tags = ["event"]

# 待办事件已处理事件
@router.put("/desposedsoftware", tags=["waitdones"])
async def despose_waitdones(res: WaitDesposeResults):
    print("despose waitdone api data:", res.cookie, res.results)
    DATABASE.hset("waitdone_despose_results", res.cookie, res.results)


@router.put("/wol")
async def magic_client(toclients=[]):
    controlor.sendwol_allclient(toclients)

# 默认按钮事件
@router.put("/addsoftwarelist")
async def addsoftwarelist(alter: Annotated[str, None]):
    softwarename, softwarepath = choose_file()
    DATABASE.lpush("softwarelist", softwarepath)
    return {"OK", softwarename}
    
@router.put("/popsoftwarelist")
async def popsoftwarelist(software):
    softwarelist = DATABASE.lrange("softwarelist")
    for i, item in enumerate(softwarelist):
        if re.match(software, item):
            DATABASE.lpop("softwarelist", i)

    return {"OK", f"POP {software}"}

@router.put("/download")
async def download(toclients=[]):
    filename, filepath = choose_file()
    with open(filepath, "rb") as f:
        controlor.sendtoclient(toclients, files=[filename, f])

    


