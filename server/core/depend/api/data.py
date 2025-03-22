import json
from typing import Annotated, AnyStr

from fastapi import(
    APIRouter,
    Query
)

from gloabl import DB
from lib import Resolver
from lib.strtool import pattern


resolver = Resolver()

# 数据接口
router = APIRouter()
prefix = "/server/data"
tags = ["data"]


@router.get("/info")
async def get_client_info(
    cln:str, 
    softname:str,
    ip: Annotated[str, None] = Query(pattern=pattern.IP)
    ):
    """
        获取不同分类下的软件信息
    """
    results = {
        "softname": softname,
        "status": False
    }
    classifylist = DB.smembers("classifylist")
    if cln not in classifylist:
        return {"ERROR": f"classify: {cln} is not exists"}
    
    info = DB.hget("heart_packages", ip)
    if info is None:
        return {"ERROR": f"client: {ip} never conected"}
    else:
        info = json.loads(info)
        results['ip'] = info['ip']
        results['mac'] = info['mac']
        conning = DB.hget("client_status", ip) == "true"
        results['conning'] = conning
        # 客户端连接时，软件才去检查软件是否启动
        if conning:
            softwares = info['softwares']
            for soft in softwares:
                if softname == soft['ecdis']['name'] and soft['conning']:
                    results['status'] = True
                else:
                    continue
    return results

@router.get("/realtime")
async def get_realtime_data():
    """
    实时更新数据，需要定期调用
        从redis中获取数据
    """
    return {
        "data": {
            "client_status": DB.hgetall("client_status"),
            "client_reports": DB.hgetall("reports"),
            "client_waitdones": DB.hgetall("waitdones"),
            "softwarelist": DB.hgetall("softwarelist"),
            "classify": DB.hgetall("classify"),
            "classifylist": DB.smembers("classifylist")
        }
    }