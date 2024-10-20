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
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
        FastAPI,
        Path,
        Depends
    )

from core import control
from projectdesposetool.start_server import SERVERMANAGE
from databasetool import RedisConn as DATABASE
from datamodel import (
    HeartPkgs,
    SoftWareCheckList,
    ShellList
    )



CONTROL = control.Control()
ORIGINS = [
    "https://localhost:8080",
    "http://localhost:8080"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

server = uvicorn.Server(uvicorn.Config(app))



# Server API

@app.get("/testapi/")
async def tapi():
    pass
    return {"msg": "Hello Server, There is Control"}

@app.put("/servers/send_control_shell")         # 发送shell指令
async def send_control_shell(shell_list: list[ShellList]):
    for shell_msg in shell_list:
    
        CONTROL.sendtoclient(shell_msg.model_dump_json())
    return shell_list# "send shell to current clients"

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


