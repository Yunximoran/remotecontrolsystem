from fastapi import Query
from typing import Annotated
from lib.strtool import pattern
from static import DB

def get_client_info(
    cln: Annotated[str, "分类名称"], 
    softname: Annotated[str, "软件名称"],
    ip: Annotated[str, Query(pattern=pattern.NET_IP)]
    ):
    """
        获取不同分类下的软件信息
    """
    mac = None
    status = False
    conning = False
    results = {
        "softname": softname,
        "status": False
    }
    classifylist = DB.smembers("classifylist")
    if cln not in classifylist:
        return None, None, None # {"ERROR": f"classify: {cln} is not exists"}
    
    info = DB.loads(DB.hget("heart_packages", ip))
    if info is None:
        return None, None, None # {"ERROR": f"client: {ip} never conected"}
    else:
        mac = info['mac']
        conning = DB.hget("client_status", ip) == "true"
        # 客户端连接时，软件才去检查软件是否启动
        if conning:
            softwares = info['softwares']
            for soft in softwares:
                if softname == soft['ecdis']['name'] and soft['conning']:
                    status = True
                else:
                    continue
    return mac, status, conning

def get_classify():
    classify = DB.loads(DB.hgetall("classify"))
    for cln in classify:
        items:list[dict] = classify[cln]
        for item in items:
            soft = item["soft"]
            ip = item["ip"]
            item['mac'], item['status'], item['conning'] = get_client_info(cln, soft, ip)
    return classify


if __name__ == "__main__":
    print(get_classify())