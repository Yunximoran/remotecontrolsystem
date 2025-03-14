import json

from ._prototype import TCP, socket
from lib.database import Redis
from lib import CatchSock
from lib.sys.processing import Process
from lib import Resolver


resolver = Resolver()
catch = CatchSock()
TCPORT = resolver("ports", "tcp", "client")
RECVSIZE = resolver("sock", "recv-size")
ENCODING = resolver("global", "encoding")

class Connector(TCP):
    
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def connect(self, ip):
        self.sock.connect((ip, TCPORT))
        
    def send(self, data: str):
        self.sock.sendall(data.encode())
        # return None

    def sendfile(self, ip,file):
        self.sock.connect((ip, TCPORT))
        # 先发送一个标识
        self.sock.sendall(file[0])
        self.sock.sendfile(file[1])
    
    # @catch.timeout
    def recv(self):
        data = self.sock.recv(RECVSIZE).decode(ENCODING)
        return data
    
    def close(self):
        self.sock.close()
        