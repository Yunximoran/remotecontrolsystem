import json
from typing import Annotated, AnyStr
from pathlib import Path
from fastapi import(
    APIRouter,
    Query
)

from static import DB
from lib import Resolver
from lib.strtool import pattern
from lib.sys.system import OS

from ._method.get import get_classify, get_net_speed

resolver = Resolver()

# 数据接口
router = APIRouter()
prefix = "/server/data"
tags = ["data"]

@router.get("/softwarelsit")
async def get_softwarelist():
    return {"softwarelist": DB.loads(DB.hgetall("softwarelist"))}   # 软件列表


@router.get("/iter_local_instructs")    # 遍历脚本目录
async def get_instructs():
    if OS == "Windows":
        suffix = r"*.bat"
    elif OS == "Linux":
        suffix = r"*.sh"
    instructs = resolver("path", "local", "instructs")
    pracpath = instructs.bind(Path.cwd())
    if pracpath.exists() and pracpath.is_dir():
        return pracpath.glob(suffix)

@router.get("/iter_local_packages") # 遍历压缩包目录
async def get_packages():
    if OS == "Windows":
        suffix = r"*.zip"
    elif OS == "Linux":
        suffix = r"*.tar"
    packages = resolver("path", "local", "packs")
    pracpath = packages.bind(Path.cwd())
    if pracpath.exists() and pracpath.is_dir():
        return pracpath.glob(suffix)

@router.get("/not_classified")
async def get_not_classified():
    classified = set(DB.hgetall("classified"))
    allclients = set(DB.hgetall("client_status"))   # 获取全部连接客户端
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
    classify = get_classify()
    return {
        "client_reports": DB.loads(DB.hgetall("reports")),        # 客户端控制运行结果汇报
        "client_waitdones": DB.loads(DB.hgetall("waitdones")),    # 客户端待办事项信息
        "instructlist": DB.loads(DB.hgetall("instructlist")),     # 预存指令列表
        "softwarelist": DB.loads(DB.hgetall("softwarelist")),
        "classify": classify,             # 分类数据
        "classifylist": DB.smembers("classifylist"),    # 分类索引
        "netspeed": get_net_speed()
    }
    
    
@router.get("/check_dirs")
async def iter_dir(base:str=None):
    path = Path(base)
    if path.exists() and path.is_dir():
        return {path.glob("*")}
    else:
        return {"ERROR": f"{base} is not exists or not a dir"}