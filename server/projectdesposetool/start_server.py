from subprocess import Popen, PIPE
import multiprocessing

import uvicorn

from projectdesposetool.parse import CONFIG
from core.api import app
from core.control import controlor
from core.udp import broadcaster

WAITDONEQUEUE = multiprocessing.Queue()


class ServerManage:
    dependencys = CONFIG.parseConfig("dependencys")
    def __init__(self) -> None:
        self.ServeList = []    # type: list[Popen]
        self.registry()
    
    def registry(self):
        self.ServeList.append(multiprocessing.Process(target=uvicorn.run,
                                                      kwargs={
                                                            "app": "core.api:app",
                                                            "host":"localhost",
                                                            "port":8000, 
                                                            "reload": True}))
        self.ServeList.append(multiprocessing.Process(target=controlor.listen))
        self.ServeList.append(multiprocessing.Process(target=broadcaster.run))
    
    def start_all_dependency(self):
        for dependency in self.dependencys.values():
            Popen(args=dependency, shell=True)

    def start(self):
        self.start_all_dependency()
        for serve in self.ServeList:
            serve.start()
        

    
    def kill(self):
        pass
    

SERVERMANAGE = ServerManage()


if __name__ == "__main__":
    SERVERMANAGE.start()
