from subprocess import Popen, PIPE
import os


from projectdesposetool.parse import CONFIG



class ServerManage:
    servers = CONFIG.parseConfig("servers")
    
    def __init__(self) -> None:
        self.ServerList = []    # type: list[Popen]
    
    def start(self):
        for shell in self.servers.values():
            self.ServerList.append(Popen(args=shell.split(" "), shell=True))
    

SERVERMANAGE = ServerManage()

