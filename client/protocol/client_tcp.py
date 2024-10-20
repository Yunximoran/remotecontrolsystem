import socket


CLIENTADDRESS = ("192.168.179.1", 8085)
SERVERADDRESS = ("192.168.179.1", 9095)


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
                print("control shell:", data)
                return data
            except TimeoutError:
                # print("time out")
                pass
            