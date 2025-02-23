import json

from fastapi import APIRouter

from datamodel import ShellList, Software
from core.depend.protocol.udp import MultiCastor
from core.depend.control import Control
# from projectdesposetool import CONFIG



multiter = MultiCastor()
controlor = Control()

# 通信接口
router = APIRouter()
prefix = "/server/send"
tags = ["send"]


@router.post("/instruct")         # 发送shell指令
async def send_control_shell(shell_list: list[ShellList], toclients: list[str] = []):
    """
        发送控制指令
    shell_list: 指令列表
    toclients: 目标地址
    """
    try:
        # 解析请求体
        instructs = [item.model_dump_json() for item in shell_list]
        # 发送控制指令
        controlor.sendtoclient(toclients, instructs=instructs) 
        return {"OK": "instructions have been sent to the client"}
    except AttributeError as e:
        return {"ERROR": e}
    

@router.post("/softwarelist")    # 发送软件清单
async def send_software_checklist(checklist: list[Software]):
    """
        发送软件清单
    checklist: 软件列表
    """
    software = [item.model_dump() for item in checklist]
    try:
        multiter.send(json.dumps(software))  
        return {"OK": "send software checklist"}
    except Exception as e:
        return {"ERROR": e}
    
