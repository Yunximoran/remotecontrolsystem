# api 接口
"""
向客户端发送软件清单
向客户端发送shell指令

通过multiprocess.Queue() 通信

向服务端发送心跳包


API 接收请求 处理请求内容 返回响应数据
服务端
"""


import time
from typing import Annotated

import uvicorn
from fastapi import (
        FastAPI,
        Path,
        Depends
    )

import control
from datamodel import (
    HeartPkgs,
    SoftWareCheckList,
    ShellList
    )
from projectdesposetool.start_server import SERVERMANAGE
from databasetool import RedisConn as DATABASE



app = FastAPI()
server = uvicorn.Server(uvicorn.Config(app))
CONTROL = control.Control()

# Server API

@app.put("/servers/send_control_shell")         # 发送shell指令
async def send_control_shell(shell_list: list[ShellList]):
    CONTROL.sendtoclient(",".join(shell_list))
    return "send shell to current clients"

@app.put("/servers/send_software_checklist")    # 发送软件清单
async def send_software_checklist(checklist: Annotated[SoftWareCheckList, None]):
    return checklist



# Client API

@app.put("/clients/send_heart_pkgs/") 
async def send_heart_pakgs(
    heart_pakgs: Annotated[HeartPkgs, None],
    ):
    # 发送心跳包
    # RedisConn.lpush("heart_list", heart_pakgs.model_dump_json())
    return heart_pakgs


