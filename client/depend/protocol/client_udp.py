import socket
import struct

from lib import Resolver

resolver = Resolver()
BROADCAST = (resolver("sock", "udp", "ip-broad"), resolver("ports", "udp", "broad"))              # 广播地址
MULTICAST = (resolver("sock", "udp", "ip-multi"), resolver("ports", "udp", "multi"))              # 组播地址

RECVSIZE = resolver("sock", "recv-size")

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
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # 允许地址复用
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     # 允许广播
        
    
    def send(self, data:str):
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
        self.join_multigroup()
    
    def join_multigroup(self):
        group = socket.inet_aton(self.multi_address)
        mreq = struct.pack("4sl", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    
    
    def send(self):
        self.sock.sendto("thi is multicast", MULTICAST)
    
    def recv(self):
        data, addr = self.sock.recvfrom(RECVSIZE)
        # 唯一能获取服务端ip的地方， 可能有用
        return data.decode()
