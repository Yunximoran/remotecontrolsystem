import socket
import struct



CLIENTADDRESS = ("192.168.179.1", 8080)

SERVER_UDP_ADDRESS = ("192.168.179.1", 8081)     # 单播地址 & 服务端地址
BROADCAST = ("<broadcast>", 8082)                # 广播地址
MULTICAST = ("224.25.25.1", 8083)                  # 组播地址

class UDP:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.init()
        self.settings()
        
    def init(self):
        pass

    def settings(self):
        pass
    
    def send(self):
        pass
    
    def recv(self):
        pass
    
    
    
class BroadCast(UDP):
    def __init__(self, address=CLIENTADDRESS):
        super().__init__() 

    def init(self):
        self.localhost, self.port = BROADCAST
        # self.sock.bind(("", self.port))       # 本机测试存在错误端口冲突，转移后可以  
        
    
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # 允许地址复用
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     # 允许广播
        
    
    def send(self, data):
        self.sock.sendto(f"1: {data}".encode(), BROADCAST)


class MultiCast(UDP):
    """
        发送数据不需要绑定bind
    """
    def __init__(self):
        super().__init__()
    
    def init(self):
        self.multi_address, self.multi_port = MULTICAST
        self.sock.bind(("", self.multi_port))
    
    def settings(self):
        group = socket.inet_aton(self.multi_address)
        mreq = struct.pack("4sl", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    
    
    def send(self):
        self.sock.sendto("thi is multicast", MULTICAST)
    
    def recv(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(data.decode())
    
