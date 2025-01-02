import struct
from .protype import UDP, socket

from projectdesposetool import CONFIG

BROADCAST = ("", )
MULTICAST = ("224.25.25.1", CONFIG.UMPORT)

class BroadCast(UDP):
    pass
        
class MultiCast:
    def __init__(self):
        self.multi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def settings(self):
        
        # 接受数据前加入组播组
        group = socket.inet_aton(MULTICAST[0])
        merq = struct.pack("4sL", group, socket.INADDR_ANY)
        self.multi.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, merq)
        
    def send(self, data:str):
        print(data)
        self.multi.sendto(data.encode(), MULTICAST)