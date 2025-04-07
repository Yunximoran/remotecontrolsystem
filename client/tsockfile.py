import socket
import multiprocessing

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.31.176", 12345))

sock.listen(5)
conn, addr = sock.accept()
def recv():
    with conn:
        data = conn.recv(1024)
        print(data.decode())
        
multiprocessing.Process(target=recv).start()
multiprocessing.Process(target=recv).start()
# with conn:
#         filename = conn.recv(1024)
#         print(filename.decode('utf-8'))
#         size = conn.recv(1024)
#         print(size.decode('utf-8'))
#         cursize= 0
#         iter = 0
#         with open(filename.decode('utf-8'), 'wb') as f: 
#             while  (cursize) < int(size.decode()):
#                 data = conn.recv(int(size.decode()))
#                 f.write(data)
#                 cursize += len(data)
#                 iter += 1
#                 print(cursize, "===", int(size.decode()))
#             print("ok")
#             print(iter)

# print("exit")