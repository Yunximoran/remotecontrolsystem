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
ENCODING = resolver("project", "encoding")

class Connector(TCP):
    
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    
    def send(self, ip, data: str):
        self.sock.connect((ip, TCPORT))
        self.sock.sendall(data.encode())
        return self.__wait_report()

    def sendfile(self, ip,file):
        self.sock.connect((ip, TCPORT))
        # 先发送一个标识
        self.sock.sendall(file[0])
        self.sock.sendfile(file[1])
        return self.__wait_report()
    
    @catch.timeout
    def __wait_report(self):
        data = self.sock.recv(RECVSIZE)
        return json.loads(data.decode(ENCODING))
        
        