import json
from typing import Annotated, AnyStr

from fastapi import(
    APIRouter,
    Query
)

from static import DB
from lib import Resolver
from lib.strtool import pattern


resolver = Resolver()

# 数据接口
router = APIRouter()
prefix = "/server/data"
tags = ["data"]


@router.get("/info")
async def get_client_info(
    cln: Annotated[str, "分类名称"], 
    softname: Annotated[str, "软件名称"],
    ip: Annotated[str, Query(pattern=pattern.NET_IP)]
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

@router.get("/not_classified")
async def get_not_classified():
    classified = set(DB.hgetall("classified"))
    allclients = set(DB.hgetall("client_status"))
    noclassified = allclients - classified
    return {
        "classified": classified,
        "notclassified": noclassified
    }


@router.get("/realtime")
async def get_realtime_data():
    """
    实时更新数据，需要定期调用
        从redis中获取数据
    """
    return {
        "client_status": DB.loads(DB.hgetall("client_status")),   # 客户端连接状态
        "client_reports": DB.loads(DB.hgetall("reports")),        # 客户端控制运行结果汇报
        "client_waitdones": DB.loads(DB.hgetall("waitdones")),    # 客户端待办事项信息
        "instructlist": DB.loads(DB.hgetall("instructlist")),     # 预存指令列表
        "softwarelist": DB.loads(DB.hgetall("softwarelist")),     # 软件列表
        "classify": DB.loads(DB.hgetall("classify")),             # 分类数据
        "classifylist": DB.smembers("classifylist")     # 分类索引
    }