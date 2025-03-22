import json
from typing import List, AnyStr
from fastapi import APIRouter

from datamodel import SoftwareList
from datamodel.instruct import InstructList
from core.depend.protocol.udp import MultiCastor
from core.depend.control import Control


multiter = MultiCastor()
controlor = Control()

# 通信接口
router = APIRouter()
prefix = "/server/send"
tags = ["send"]


@router.post("/instruct") 
async def send_control_shell(instructlist: InstructList, toclients: List[AnyStr] = []):
    """
        发送控制指令
    shell_list: 指令列表 
    toclients: 目标地址
    """
    try:
        
        # 解析请求体
        instructs = [item.model_dump_json() for item in instructlist.items]
        # 发送控制指令
        controlor.sendtoclient(toclients, instructs=instructs) 
        return {"OK": "instructions have been sent to the client"}
    except Exception as e:
        print(e)
        return {"ERROR": e}
    

@router.post("/softwarelist")    # 发送软件清单
async def send_software_checklist(checklist: SoftwareList):
    """
        发送软件清单
    checklist: 软件列表
    """
    
    softwares = json.dumps([item.model_dump() for item in checklist.items], ensure_ascii=False)
    
    try:
        multiter.send(softwares)  
        return {"OK": f"send software checklist {softwares}"}
    except Exception as e:
        return {"ERROR": e}
    
