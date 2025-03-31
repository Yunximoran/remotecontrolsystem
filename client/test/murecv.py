import socket
import struct

MCAST_GRP = '224.3.29.71'
MCAST_PORT = 20002
IFACE_IP = '192.168.6.1'  # 改为接收端实际IP

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

# 显式指定网络接口加入组播组
mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton(IFACE_IP))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Listening for multicast messages on {MCAST_GRP}:{MCAST_PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Received from {addr}: {data.decode()}")