import socket

from despose import CONFIG


CLIENTADDRESS = (CONFIG.IP, CONFIG.TCPORT)


class TCP:
    def __init__(self, timeout=1):
        self.init()
        self.settings(timeout)
    
    
    def init(self):
        # 初始化TCP套接字，绑定本机地址
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(CLIENTADDRESS)
        
    
    def settings(self, timeout):
        self.sock.settimeout(timeout)
        
    
    def listening(self):
        self.sock.listen(5)
        while True:
            try:
                server_sock, address = self.sock.accept()
                data = server_sock.recv(1024)
                return data.decode()
            except TimeoutError:
                # print("time out")
                pass
            