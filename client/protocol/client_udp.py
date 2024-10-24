import socket
import struct
import json

from despose import CONFIG


BROADCAST = ("<broadcast>", CONFIG.UBPORT)                # 广播地址
MULTICAST = ("224.25.25.1", CONFIG.UMPORT)                  # 组播地址

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
    def __init__(self):
        super().__init__() 

    def init(self):
        self.localhost, self.port = BROADCAST
        
    
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # 允许地址复用
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     # 允许广播
        
    
    def send(self, data):
        self.sock.sendto(data.encode(), BROADCAST)


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
        data, addr = self.sock.recvfrom(1024)
            # 唯一能获取服务端ip的地方， 可能有用
        return data.decode()
