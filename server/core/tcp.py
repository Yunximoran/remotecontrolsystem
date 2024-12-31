import socket
import time

from projectdesposetool import CONFIG

class TCP:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.settings()
        
    def settings(self):
        pass
    
    
class TCPConnect(TCP):
        
    def settings(self):
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    
    def send(self, shell:str, ip):
        # print(shell, type(shell))
        try: 
            self.tcp_socket.connect((ip, CONFIG.TCPORT))
            self.tcp_socket.sendall(shell.encode())
            data = self.tcp_socket.recv(1024)
            return data.decode('utf-8')
        except ConnectionRefusedError:
            print("当前无连接")
        finally:
            self.tcp_socket.close()
    
    

class TCPListen(TCP):
    def settings(self):
        self.tcp_socket.bind((CONFIG.IP, CONFIG.TSPORT))
        self.tcp_socket.listen(5)
        self.tcp_socket.settimeout(1)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    
    def recv(self):
        client_sock, address = self.tcp_socket.accept()
        # client_sock.settimeout(1000)
        data = client_sock.recv(1024)
        return client_sock, address, data.decode()


        