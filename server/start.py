from typing import Tuple, Any, List

import uvicorn

from core.depend.protocol.tcp import TCPListen
from core.depend.protocol.udp import UDP, MultiCast
from projectdesposetool.catchtools import Catch
from projectdesposetool.systool.custprocess import MultiProcess


class ServerManage:
    Tasks: List[MultiProcess] = []
    def __init__(self) -> None:
        __tcplisten = TCPListen()
        __broadcaster = UDP()

        self.__registry((
            __tcplisten.listen,  # TCP监听
            __broadcaster.run,   # UDP监听
        ))
        
        self.__starttasks()
    
    def __registry(self, tasks: Tuple[Any]):
        # 注册依赖任务 
        for task in tasks:
            self.Tasks.append(MultiProcess(target=task))

    def __starttasks(self):
        for server in self.Tasks:
            server.start()
            
    def run(self):
        uvicorn.run("core.app:APP", host="127.0.0.1", port=8000, reload=True)    

if __name__ == "__main__":
    """
    多进程会被
    """
    server_manager = ServerManage()
    server_manager.run()
    
