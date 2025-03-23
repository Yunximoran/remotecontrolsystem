import socket
from lib.sys import NetWork

broadcast_address='255.255.255.255'
port=7
# 00505624DF2B
magic = NetWork.create_magic_packet("00:50:56:24:DF:2B")
print(magic)


# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# sock.sendto(magic, ("0.0.0.0", 2))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magic, (broadcast_address, port))