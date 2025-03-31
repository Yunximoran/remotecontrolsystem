from multiprocessing import Process

from lib import Resolver
from ._base import *
from ..system import SYSTEM

logger = Logger("ConnectServe", "connect.log")



class ConnectServe(BaseServe):

    def serve(self):
        # 每秒广播心跳包数据
        print("Connect Serve Started")
        udp_conn = BroadCast(LISTENPORT_1)
        while True:
            time.sleep(1)
            self.update_soft_status()
            heart_pkgs = self.get_heartpack()
            
            logger.record(1, f"heart packages: {heart_pkgs}")
            context = json.dumps(heart_pkgs, ensure_ascii=False, indent=4)
            udp_conn.send(context, (BROADADDR, LISTENPORT_1))   
            
        
    def get_heartpack(self) -> str:
        """
            格式化心跳包数据
        """
        with open(PATH_MAP_SOFTWARES, "r", encoding='utf-8') as f:
            softwares = json.load(f)
        return {
            "ip": IP,
            "mac": MAC,
            "softwares": softwares
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