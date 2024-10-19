import socket
import struct



CLIENTADDRESS = ("192.168.179.1", 8080)

SERVER_UDP_ADDRESS = ("192.168.179.1", 8081)     # 单播端口 & 服务端地址
BROADCAST = ("<broadcast>", 8082)                # 广播端口
MULTICAST = ("224.0.0.1", 8083)                  # 组播端口



class UDP:
    def __init__(self, address=CLIENTADDRESS):
        self.address = address
        self.localhost, self.port = address
        
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)    
        
        self.init()
    
    
    def init(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        # self.receive()
        
    
    def send(self, data):
        self.sock.sendto(f"0: {data}".encode(), SERVER_UDP_ADDRESS)
        self.sock.sendto(f"1: {data}".encode(), BROADCAST)
    
        
    def __send_heartpackage(self):
        self.sock.sendto(f"the is heart package data from client:{self.address}")
    
    
    def recv(self):
        data, _ = self.sock.recvfrom(1024)
        print(_)
        return data.decode()


    def receive(self):
        group = socket.inet_aton("224.0.0.0")
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)   
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


