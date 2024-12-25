# api 接口
"""
向客户端发送软件清单
向客户端发送shell指令

通过multiprocess.Queue() 通信

向服务端发送心跳包


API 接收请求 处理请求内容 返回响应数据
服务端
"""

import json
import asyncio
import re

from typing import Annotated

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
        FastAPI,
        HTTPException,    
        WebSocket,
        WebSocketDisconnect
        )

from core import control
from core.udp import MultiCast
from databasetool import DataBaseManager as DATABASE
from datamodel import (
    NewUser,
    ShellList,
    Software,
    Waitdone,
    Credentils
    )
from projectdesposetool import SERVERMANAGE
from projectdesposetool.systool import choose_software





ORIGINS = [
    # vue address
    "https://localhost:8080",
    "http://localhost:8080",
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



@app.websocket("/ws")
async def predict(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            client_status = DATABASE.hgetall("client_status")
            client_reports = DATABASE.hgetall("reports")
            client_waitdones = DATABASE.hgetall("waitdones")
            
            softwarelist = DATABASE.lrange("softwarelist")
            await websocket.send_json([client_status, client_reports, client_waitdones, softwarelist])
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("链接中断")


@app.put("/servers/despose/waitdone/")
async def despose_waitdones(res: Waitdone):
    try:
        controlor.dps_waitdone(res.msg, res.results)
    except Exception as e:
        print(e)
        
    
# LOGIN
@app.post("/servers/login/")
async def login(loginform: Credentils):
    credentils = loginform.account
    password = loginform.password
    accounts_information = DATABASE.hget("accounts", credentils)
    if accounts_information is not None:
        if password == accounts_information['password']:
            return {"start": "OK", "msg": accounts_information}
        else:
            raise HTTPException(status_code=404, detail="password is error")
    else:
        raise HTTPException(status_code=404, detail="account is not exits")
    


# SEND TO CLIENT
@app.put("/servers/send_control_shell/")         # 发送shell指令
async def send_control_shell(shell_list: list[ShellList], toclients: list[str] = []):
    try:
        for shell_msg in shell_list:
            
            controlor.sendtoclient(shell_msg.model_dump_json(), toclients)
            
        return {"ok": "send a shell to client"}
    except Exception as e:
        return {"ERROR": e}
    

@app.put("/servers/send_software_checklist/")    # 发送软件清单
async def send_software_checklist(checklist: list[Software]):
    software = [item.model_dump() for item in checklist]
    try:
        multiter.send(json.dumps(software))  
        return {"OK": "send software checklist"}
    except Exception as e:
        return {"ERROR": e}
    
    
# DATA
@app.get("/servers/data/client_status")
async def getclientmessage():   # 获取客户端连接状态
    clients = DATABASE.hgetall("client_status")
    return clients

@app.get("/servers/data/accounts/")
async def get_account_data(account: Annotated[str, None]):
    # 从数据库中获取账号数据，校验账号是否存在
    account_infomation = DATABASE.hget("accounts", account)
    if account_infomation is not None:
        return json.loads(account_infomation)
    
    return {'start': "not data"}


@app.put("/servers/data/registry_new_account")
async def registryaccount(regisform: NewUser):
    # 注册新用户，保存在数据库
    DATABASE.hset("accounts", regisform.account, regisform.model_dump_json())   
    return {
        "account": regisform.account,
        "username": regisform.username
        
    }
    
@app.get("/servers/data/softwarelist")
async def get_softwarelist():
    return DATABASE.hgetall("softwarelist")

# ALTER #
# config
@app.put("/servers/settings/alter/")
async def alter_settings(option: str, nval: str):
    # 修改服务端配置
    return {"ok": f"reset {option} => {nval}"}

# data
@app.put("/servers/data/alter/")
async def alter_software(alter: Annotated[str, None]):
    if alter == "push":
        software = choose_software()
        DATABASE.lpush("softwarelist", software)
        return {"OK": software}






