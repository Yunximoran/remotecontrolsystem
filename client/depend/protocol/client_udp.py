import socket
import struct

from lib import Resolver

resolver = Resolver()

BROADADDR = resolver("sock", 'udp', "ip-broad")
MULTIADDR = resolver("sock", "udp", "ip-multi")

LISTENPORT_1 = resolver("ports", "udp", "broad")
LISTENPORT_2 = resolver("ports", "udp", "multi")


TTL = 10

USENET = resolver("network", "ip")
# USEPORT = resolver("port")
RECVSIZE = resolver("sock", "recv-size")
ENCODING = resolver("global", 'encoding')

__all__ = [
    "LISTENPORT_1",
    "LISTENPORT_2",
    
    "BROADADDR",
    "RECVSIZE",
    "ENCODING"
]
class UDP:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.settings()
        self.init(cast=(USENET, port))

        
    def init(self, cast):
        self.sock.bind(cast)

    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # 允许地址复用
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)     # 允许广播
    
    def send(self, data:str, cast:tuple):
        self.sock.sendto(data.encode(ENCODING), cast)
    
    def recv(self):
        data, addr = self.sock.recvfrom(RECVSIZE)
        return data.decode(ENCODING), addr
    
    
    
class BroadCast(UDP):
    def __init__(self, port):
        super().__init__(port) 
            
    def send(self, data:str, cast:tuple):
        self.sock.sendto(data.encode(ENCODING), cast)
        
    def recv(self):
        data, addr = self.sock.recvfrom(RECVSIZE)
        return data.decode(ENCODING), addr

class MultiCast(UDP):
    """
    """
    def __init__(self, port):
        super().__init__(LISTENPORT_2)
    
        
    def __join_multigroup(self):
        # 加入组播组
        group = socket.inet_aton(MULTIADDR)
        mreq = struct.pack("4sl", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)    
    
    def __set_TTL(self):
        self.sock.setsockopt(socket.SOCK_DGRAM, socket.IP_MULTICAST_TTL, TTL)
        
    def send(self, cast):
        self.sock.sendto("there is multicaster", cast)
    
    def recv(self):
        self.__join_multigroup()
        data, addr = self.sock.recvfrom(RECVSIZE)
        # 唯一能获取服务端ip的地方， 可能有用
        return data.decode(ENCODING), addr
