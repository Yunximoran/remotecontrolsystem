from subprocess import Popen, PIPE

from projectdesposetool.parse import CONFIG



class ServerManage:
    servers = CONFIG.parseConfig("servers")
    
    def __init__(self) -> None:
        self.ServerList = []
    
    def start(self):
        for shell in self.servers.values():
            self.ServerList.append(Popen(args=shell, stdin=PIPE))
    
    def kill(self):
        while self.ServerList != []:
            process = self.ServerList.pop()
            Popen.kill(process)

SERVERMANAGE = ServerManage()

