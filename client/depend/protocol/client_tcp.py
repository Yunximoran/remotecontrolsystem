import socket

from lib import Resolver
resolver = Resolver()
TIMEOUT = resolver("sock", "tcp", "timeout")
RECVSIZE = resolver("sock", "recv-size")
ENCODING = resolver("global", 'encoding')

IP = resolver("network", "ip")
IPSERVER = resolver("network", "ip-server")

TCPORT = resolver("ports", "tcp", "client")
TSPORT = resolver("ports", "tcp", "server")

class TCP:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.settings()
    
    def settings(self):
        pass
    
    def send(self, data:str):
        self.sock.sendall(data.encode())
    
    def recv(self):
        return self.sock.recv(RECVSIZE)

    def close(self):
        self.sock.close()
    
class TCPListen(TCP):
    def __init__(self, ip=IP, port=TCPORT):
        super().__init__()
        self.address = (ip, port)
        self.sock.bind(self.address)
        self.sock.listen(5)
    
    
    def settings(self):
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(TIMEOUT)
    
    def accept(self):
        return self.sock.accept()
    
    
    def recv(self):
        server_sock, server_address = self.sock.accept()
        data = server_sock.recv(RECVSIZE)
        return (server_sock, data.decode())

class TCPConnect(TCP):
    def __init__(self):
        super().__init__()
        
    def send(self, data):
        self.sock.connect((IPSERVER, TSPORT))
        self.sock.sendall(data.encode(ENCODING))
        


if __name__ == "__main__":
    TCPListen()