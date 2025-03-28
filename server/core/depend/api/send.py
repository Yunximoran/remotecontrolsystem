import json
from typing import List, AnyStr
from fastapi import APIRouter

from datamodel import SoftwareList
from datamodel.instruct import InstructList, Instruct
from core.depend.protocol.udp import MultiCastor
from core.depend.control import Control

from static import DB


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

@router.post("/start_all_softwares")
async def start_all_softwares():
    context = DB.hgetall("classify")
    classify = DB.loads(context)
    ip_soft: dict[str, list] = {}
    
    # 遍历所有分类
    for cln in classify:
        data = classify[cln]
        for item in data:
            soft = item['soft']
            ip = item['ip']
            # 统计每个ip 对应的软件构造成指令列表
            if ip not in ip_soft:
                ip_soft[ip] = []
            ip_soft[ip].append(Instruct(label="start -s", instruct=soft).model_dump_json())
    
    for ip in ip_soft:
        controlor.sendtoclient([ip], instructs=ip_soft[ip])

@router.post("/close_all_softwares")
async def close_all_softwares():
    context = DB.hgetall("classify")
    classify = DB.loads(context)
    ip_soft: dict[str, list] = {}
    
    # 遍历所有分类
    for cln in classify:
        data = classify[cln]
        for item in data:
            soft = item['soft']
            ip = item['ip']
            # 统计每个ip 对应的软件构造成指令列表
            if ip not in ip_soft:
                ip_soft[ip] = []
            ip_soft[ip].append(Instruct(label="close -s", instruct=soft).model_dump_json())
    
    for ip in ip_soft:
        controlor.sendtoclient([ip], instructs=ip_soft[ip])