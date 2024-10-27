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
import json
from typing import Annotated

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
        FastAPI,
        Path,
        Depends
    )

from core import control
from core.udp import MultiCast
from datamodel import (
    HeartPkgs,
    ShellList,
    SoftWare
    )




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

controlor = control.Control()
multiter = MultiCast()

# Server API

@app.get("/testapi/")
async def tapi():
    pass
    return {"msg": "Hello Server, There is Control"}

@app.put("/servers/send_control_shell/")         # 发送shell指令
async def send_control_shell(shell_list: list[ShellList]):
    try:
        # print(shell_list, type(shell_list))
        for shell_msg in shell_list:
            # print(shell_msg)
            controlor.sendtoclient(shell_msg.model_dump_json())
        return {"ok": "send a shell to client"}
    except Exception as e:
        return {"ERROR": e}

@app.put("/servers/send_software_checklist/")    # 发送软件清单
async def send_software_checklist(checklist: list[SoftWare]):
    software = [item.model_dump() for item in checklist]
    try:
        multiter.send(json.dumps(software))  
        return {"OK": "send software checklist"}
    except Exception as e:
        return {"ERROR": e}



