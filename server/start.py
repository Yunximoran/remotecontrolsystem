from typing import Tuple, Any, List

import uvicorn

from core.depend.protocol.tcp import Listener
from projectdesposetool import CONFIG
from projectdesposetool.catchtools import Catch
from projectdesposetool.systools.processing import Process
from core.depend.protocol.udp import BroadCastor


# FASTAPI设置常量
FASTAPP = "core.app:APP"
FASTHOST = "127.0.0.1"
FASTPORT = 8000
ISRELOAD = True

# 监听设置常量
SERVERADDRESS = (CONFIG.IP, CONFIG.TSPORT)
LISTENES = 5

# 广播设置常量
BROADCAST = ("0.0.0.0", CONFIG.UBPORT)              # 配置UDP广播地址
MULTICAST = ("224.25.25.1", CONFIG.UMPORT)          # 配置UDP组播地址


class Start:
    Tasks: List[Process] = []
    def __init__(self) -> None:
        self.__registry((
            self._tcplisten,
            self._udplisten,
        ))
        
        self.__starttasks()
        uvicorn.run(app=FASTAPP, host=FASTHOST, port=FASTPORT, reload=ISRELOAD)
        self.__jointasks()
    
    def _tcplisten(self):
        Listener(SERVERADDRESS, LISTENES).listen()
    
    def _udplisten(self):
        BroadCastor(BROADCAST).listen()
        
    def __registry(self, tasks: Tuple[Any]):
        # 注册依赖任务 
        for task in tasks:
            self.Tasks.append(Process(target=task))

    def __starttasks(self):
        for server in self.Tasks:
            server.start()
            
        
    def __jointasks(self):
        for server in self.Tasks:
            server.join()


if __name__ == "__main__":
    """
    多进程会被
    """
    Start()
