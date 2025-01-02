import json

from fastapi import APIRouter

from datamodel import ShellList, Software
from core.depend.protocol.udp import MultiCast
from core.depend import control

multiter = MultiCast()
controlor = control.Control()

router = APIRouter()

# SEND TO CLIENT
@router.post("/sends/instruct/", tags=["send", "instruct"])         # 发送shell指令
async def send_control_shell(shell_list: list[ShellList], toclients: list[str] = []):
    try:
        for shell_msg in shell_list:
            controlor.sendtoclient(shell_msg.model_dump_json(), toclients)
            
        return {"ok": "send a shell to client"}
    except Exception as e:
        return {"ERROR": e}
    

@router.post("/sends/softwarelist/", tags=["send", "softwarelist"])    # 发送软件清单
async def send_software_checklist(checklist: list[Software]):
    software = [item.model_dump() for item in checklist]
    try:
        multiter.send(json.dumps(software))  
        return {"OK": "send software checklist"}
    except Exception as e:
        return {"ERROR": e}
    

@router.post("/sends/buttons/", tags=["button"])
async def default_control(btype: str):
    if btype == "push -s":
        pass
    
    if btype == "pop -s":
        pass

    if btype == "close -s":
        pass
    
    if btype == "download":
        pass
    