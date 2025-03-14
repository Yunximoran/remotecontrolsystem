# alter 修改一些配置选项

from fastapi import APIRouter
from lib import Resolver

resolver = Resolver()
# 接口信息
router = APIRouter()
prefix = "/server/alter"
tags = ["alter"]


# 修改设置选项
@router.put("/settings/port/")
async def alter_settings(sock: str, option: str, nval: str):
    # 修改端口设置
    """
    sock: tcp | udp
    option: 选型 [server] | [client]
    nval: 新值
    """
    ports = resolver("ports", option)
    ports.setdata(nval)
    """
        重启后生效吗？
    """
    return {"ok": f"reset {option} => {nval}"}

