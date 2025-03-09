import socket

from lib import Resolver

resolver = Resolver()

ADDRESS = resolver("network", "ip")
TSPORT = resolver("ports", "tcp", "server")

print(ADDRESS, TSPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((ADDRESS, TSPORT))
sock.listen(5)

while True:
    s, addr = sock.accept()
    
    d1 = s.recv(1024)
    
    s.sendall(b"dw")
    