import json

from fastapi import APIRouter

from datamodel import ShellList, Software
from core.depend.protocol.udp import MultiCast
from core.depend.control import Control

multiter = MultiCast()
controlor = Control()

# 通信接口
router = APIRouter()


@router.post("/instruct", tags=["send", "instruct"])         # 发送shell指令
async def send_control_shell(shell_list: list[ShellList], toclients: list[str] = []):
    try:
        instructs = [item.model_dump_json() for item in shell_list]
        controlor.sendtoclient(toclients, instructs=instructs) 
        return {"OK": "instructions have been sent to the client"}
    except AttributeError as e:
        return {"ERROR": e}
    

@router.post("/softwarelist", tags=["send", "softwarelist"])    # 发送软件清单
async def send_software_checklist(checklist: list[Software]):
    software = [item.model_dump() for item in checklist]
    try:
        multiter.send(json.dumps(software))  
        return {"OK": "send software checklist"}
    except Exception as e:
        return {"ERROR": e}
    
