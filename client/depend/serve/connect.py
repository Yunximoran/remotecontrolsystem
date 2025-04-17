from pathlib import Path
from multiprocessing import Process


from lib.sys import NetWork
from lib.sys.sock.udp import BroadCastor
from ._base import *

logger = Logger("ConnectServe", "connect.log")

# 广播地址
BROADADDR = resolver("sock", 'udp', "ip-broad")

# 绑定广播使用网卡
LISTENPORT_1 = resolver("ports", "udp", "broad")
PATH = resolver("local")


class ConnectServe(BaseServe):

    def serve(self):
        # 每秒广播心跳包数据
        print("Connect Serve Started")
        udp_conn = BroadCastor((IP, LISTENPORT_1))    # 发送端广播
        while True:
            self.update_soft_status()
            heart_pkgs = self.get_heartpack()
            
            logger.record(1, f"heart packages: {heart_pkgs}")
            context = json.dumps(heart_pkgs, ensure_ascii=False, indent=4)
            udp_conn.send(context, (BROADADDR, LISTENPORT_1))   
            
        
    def get_heartpack(self) -> str:
        """
            格式化心跳包数据
        """
        # PATH_MAP_SOFTWARES
        with open(PATH_MAP_SOFTWARES, "r", encoding='utf-8') as f:
            softwares = json.load(f)

        with open(PATH_MAP_FILES, 'r', encoding="utf-8") as f:
            mapfiles = json.load(f)
        
        return {
            "ip": IP,
            "mac": MAC,
            "os": OS,
            "netspeed": NetWork.check_speed(resolver("network").attrib["name"]),
            "softwares": softwares,
            "working": str(Path.cwd()),
            "files": {file: mapfiles[file]['status'] for file in mapfiles}
        }
        
    def update_soft_status(self):
        with open(PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
            softwares = json.load(f)
            for soft in softwares:
                info = soft['ecdis']
                pracpath = info['prac-path']
                soft['conning'] = True if SYSTEM._check_soft_status(pracpath) else False
        
        with open(PATH_MAP_SOFTWARES, 'w', encoding='utf-8') as f:
            json.dump(softwares, f, ensure_ascii=False, indent=4)