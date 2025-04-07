import socket
from pathlib import Path
import multiprocessing

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# def con(D):
#     sock.connect(("192.168.31.176", 12345))
#     for i in range(10):
#         sock.sendall(D)
    

# multiprocessing.Process(target=con, args=("hello", )).start()
# multiprocessing.Process(target=con, args=("world", )).start()


path = Path("./test/Clash.zip")
# print(path.exists())
# print(path.name)
# print(path.stat().st_size)
# sock.sendall(path.name.encode())
# sock.sendall(str(path.stat().st_size).encode())

with open(path, 'rb') as f:
    print(type(f))

# sock.close()
# # sock.sendall("exit".encode())

