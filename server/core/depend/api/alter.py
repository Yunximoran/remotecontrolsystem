from typing import Annotated

from fastapi import APIRouter

from projectdesposetool import choose_software
from databasetool import DataBaseManager as DATABASE
from datamodel import WaitDesposeResults

router = APIRouter()

# 修改设置选项
@router.put("/alter/settings/port/", tags=["settings", "port"])
async def alter_settings(option: str, nval: str):
    # 修改服务端配置
    return {"ok": f"reset {option} => {nval}"}

# 修改本地数据
@router.put("/alter/data", tags=["data"])
async def alter_software(alter: Annotated[str, None]):
    if alter == "push":
        software = choose_software()
        DATABASE.lpush("softwarelist", software)
        return {"OK": software}

@router.put("/default/control")
async def default_control(btype: str):
    if btype == "push -s":
        pass
    
    if btype == "pop -s":
        pass

    if btype == "close -s":
        pass
    
    if btype == "download":
        pass

@router.put("/alter/waitdones/", tags=["waitdones"])
async def despose_waitdones(res: WaitDesposeResults):
    print("despose waitdone api data:", res.cookie, res.results)
    DATABASE.hset("waitdone_despose_results", res.cookie, res.results)
