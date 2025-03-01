import json

from ._prototype import TCP, socket
from databasetool import Redis
from dispose import CONFIG
from dispose import Catch
from dispose.sys.processing import Process


class Connector(TCP):
    
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def catchtimeout(func):
        def wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
                data = self.sock.recv(1024)
                return json.loads(data.decode('utf-8'))
            except ConnectionAbortedError:
                print("当前无连接")
            finally:
                self.sock.close()
        return wrapper
    
    @catchtimeout
    def send(self, ip, data: str):
        self.sock.connect((ip, CONFIG.TCPORT))
        self.sock.sendall(data.encode())
        

    @catchtimeout
    def sendfile(self, ip,file):
        self.sock.connect((ip, CONFIG.TCPORT))
        self.sock.sendall(file[0])
        self.sock.sendfile(file[1])
        
        