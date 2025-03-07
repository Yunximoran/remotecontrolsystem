import socket

from lib import Resolver
resolver = Resolver()
TIMEOUT = 1
RECVSIZE = resolver("sock", "recv-size")
IP = resolver("network", "ip")
SERVERIP = '192.168.6.1'
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
        self.sock.settimeout(TIMEOUT)
    
    
    def listening(self):
        """
        :type server_socket: socket.socket
        :return 
        """
        while True:
            try:
                server_sock, self.saddr = self.sock.accept()
                data = server_sock.recv(2048)
                return (server_sock, data.decode())
            except TimeoutError:
                pass
    
    def recv(self):
        server_sock, server_address = self.sock.accept()
        data = server_sock.recv(2048)
        return (server_sock, data.decode())

class TCPConnect(TCP):
    def __init__(self):
        super().__init__()
        
    def send(self, data):
        # TSPORT: 9095
        self.sock.connect((SERVERIP, TSPORT))
        self.sock.sendall(data.encode())
        


if __name__ == "__main__":
    TCPListen()