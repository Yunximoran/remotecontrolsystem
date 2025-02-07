import multiprocessing

import uvicorn

from core.depend.protocol.tcp import TCPListen
from core.depend.protocol.udp import UDP, MultiCast
from projectdesposetool.catchtools import Catch

multiter = MultiCast()
broadcaster = UDP()


class ServerManage:
    Tasks = []
    def __init__(self) -> None:
        self.tcplisten = TCPListen()  # 将 tcplisten 作为类的属性
        self.registry()
    
    def registry(self):
        # 启动TCP监听
        self.Tasks.append(multiprocessing.Process(target=self.tcplisten.listen))
        # 启动UDP广播
        self.Tasks.append(multiprocessing.Process(target=broadcaster.run))
    
    def run_fastapi(self):
        uvicorn.run("core:app", host="0.0.0.0", port=8000, reload=True)
    
    def run(self):
        self.start_servers()
        self.run_fastapi()
        
    @Catch.process(tasks=Tasks)
    def start_servers(self):
        for server in self.Tasks:
            server.start()
    

if __name__ == "__main__":
    """
    多进程会被
    """
    server_manager = ServerManage()
    server_manager.run()
    
