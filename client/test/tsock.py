import socket
import time

from lib import Resolver

resolver = Resolver()

SERVERIP = resolver("network", "ip-server")
TSPORT = resolver("ports", "tcp", "server")
print(SERVERIP, TSPORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVERIP, TSPORT))
while True:
    
    sock.send(b"hello world")

    d2 = sock.recv(1024)
    print("回复", d2.decode())