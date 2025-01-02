from typing import Annotated

from fastapi import APIRouter

from projectdesposetool import choose_software
from databasetool import DataBaseManager as DATABASE

# 修改接口
router = APIRouter()

# 修改设置选项
@router.put("/settings/port/", tags=["settings", "port"])
async def alter_settings(option: str, nval: str):
    # 修改服务端配置
    return {"ok": f"reset {option} => {nval}"}
