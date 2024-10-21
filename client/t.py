import socket
import struct

class UDP:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind("")
        
    def settings(self):
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        

# 发送者
def multicast_sender(message, multicast_group=('224.0.0.1', 5004)):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
    sock.sendto(message.encode(), multicast_group)

# 接收者
def multicast_receiver(group='224.0.0.1', port=5004):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    
    # 加入组播组
    group = socket.inet_aton(group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"接收到来自 {addr} 的消息: {data.decode()}")

# 示例调用
# 若要发送消息，请调用: multicast_sender('Hello, Multicast!')
# 若要接收消息，请调用: multicast_receiver()
