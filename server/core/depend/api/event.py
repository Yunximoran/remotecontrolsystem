from typing import Annotated

from fastapi import APIRouter

from projectdesposetool import choose_software
from databasetool import DataBaseManager as DATABASE
from datamodel import WaitDesposeResults

# 事件接口
router = APIRouter()

# 待办事件已处理事件
@router.put("/event/desposed_waitdones/", tags=["waitdones"])
async def despose_waitdones(res: WaitDesposeResults):
    print("despose waitdone api data:", res.cookie, res.results)
    DATABASE.hset("waitdone_despose_results", res.cookie, res.results)


# 默认按钮事件
@router.put("/addsoftwarelist", tags=["softwares"])
async def addsoftwarelist(alter: Annotated[str, None]):
    software = choose_software()
    DATABASE.lpush("softwarelist", software)
    return {"OK", software}
    
@router.put("/popsoftwarelist", tags=["softwares"])
async def popsoftwarelist():
    pass

@router.put("/close_clients", tags=["client"])
async def client_close():
    pass

@router.put("/restart_clients", tags=["client"])
async def client_restart():
    pass

@router.put("/download", tags=["client"])
async def download():
    pass


