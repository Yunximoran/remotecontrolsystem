import socket


from ._prototype import TCP
from projectdesposetool.catchtools import Catch


class Listener(TCP):
    def __init__(self, fimaly=socket.AF_INET, type=socket.SOCK_STREAM):
        super().__init__(fimaly, type)
    def init(self, addr, timeout=1):
        self.timeout = timeout
        self.sock.bind(addr)
        
    def setting(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(self.timeout)
        
    
if __name__ == "__main__":
    pass