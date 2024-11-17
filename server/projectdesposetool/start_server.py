from subprocess import Popen, PIPE
import os


from projectdesposetool.parse import CONFIG



class ServerManage:
    servers = CONFIG.parseConfig("servers")
    
    def __init__(self) -> None:
        self.ServerList = []    # type: list[Popen]
    
    def start(self):
        for shell in self.servers.values():
            self.ServerList.append(Popen(args=shell, stdin=PIPE, shell=True))
    
    def kill(self):
        for process in self.ServerList:
            print(process)

SERVERMANAGE = ServerManage()

