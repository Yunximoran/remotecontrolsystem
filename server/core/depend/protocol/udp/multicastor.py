import struct
from ._prototype import UDP, socket

from lib import Resolver

resolver = Resolver()

# "224.25.25.1"
MULTICAST = (resolver("sock", "udp", "ip-multi"), resolver("ports", "udp", "multi"))


        
class MultiCastor(UDP):
    def __init__(self):
        super().__init__()
    
    def settings(self):
        # 设置组播TTL
        ttl = struct.pack('b', 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
    def join_group(self):
        
        # 接受数据前加入组播组
        group = socket.inet_aton(MULTICAST[0])
        merq = struct.pack("4sL", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, merq)
        
    def send(self, data:str):
        self.sock.sendto(data.encode(), MULTICAST) 