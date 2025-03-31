import socket
import time

MCAST_GRP = '224.3.29.71'
MCAST_PORT = 20002

# 创建UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

while True:
    message = f"Multicast message at {time.strftime('%Y-%m-%d %H:%M:%S')}"
    sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
    print(f"Sent: {message}")
    time.sleep(2)