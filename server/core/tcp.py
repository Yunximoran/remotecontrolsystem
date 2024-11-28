import socket
import time

from projectdesposetool import CONFIG



class TCP:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    
    def send(self, shell:str, ip):
        print(shell, type(shell))
        try: 
            self.tcp_socket.connect((ip, CONFIG.TCPORT))
            self.tcp_socket.sendall(shell.encode())
        except ConnectionRefusedError:
            print("当前无连接")
        finally:
            self.tcp_socket.close()
    
    def close(self):
        self.tcp_socket.close()
        