from typing import Tuple, Any, List
import uvicorn

from core.depend.protocol.tcp import Listener
from core.depend.protocol.udp import BroadCastor

from lib.sys.processing import Process
from lib import Resolver

resolver = Resolver()

# FASTAPI设置常量
FASTAPP = resolver("server", "app")
FASTHOST = resolver("server", "host")
FASTPORT = resolver("server", "port")
ISRELOAD = resolver("server", "reload")

# 监听设置常量
SERVERADDRESS =(resolver("network", "ip"), resolver("ports", "tcp", "server"))
LISTENES = resolver("sock", "tcp", "listenes")


# 广播设置常量
BROADCAST = (resolver("sock", "udp", "ip-broad"), resolver("ports", "udp", "broad"))    # 配置UDP广播地址



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
