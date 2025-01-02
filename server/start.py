import multiprocessing

import uvicorn

from core.depend.protocol.tcp import TCPListen
from core.depend.protocol.udp import UDP, MultiCast

WAITDONEQUEUE = multiprocessing.Queue()

multiter = MultiCast()
broadcaster = UDP()

class ServerManage:
    def __init__(self) -> None:
        self.ServeList = []    # type: list[multiprocessing.Process]
        self.tcplisten = TCPListen()  # 将 tcplisten 作为类的属性
        self.registry()
    
    def registry(self):
        # 启动fastapi
        self.ServeList.append(multiprocessing.Process(target=self.run_fastapi))
        # 启动TCP监听
        self.ServeList.append(multiprocessing.Process(target=self.tcplisten.listen))
        # 启动UDP广播
        self.ServeList.append(multiprocessing.Process(target=broadcaster.run))
    
    def run_fastapi(self):
        uvicorn.run("core:app", host="0.0.0.0", port=8000, reload=True)
    
    def start_servers(self):
        for server in self.ServeList:
            server.start()
        for server in self.ServeList:
            server.join()

if __name__ == "__main__":
    server_manager = ServerManage()
    server_manager.start_servers()
