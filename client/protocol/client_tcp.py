import socket

from despose import CONFIG


class TCP:
    def __init__(self, ip=CONFIG.IP, port=CONFIG.TCPORT, timeout=1):
        self.address = (ip, port)
        
        self.init()
        self.settings(timeout)
    
    def init(self):
        # 初始化TCP套接字，绑定本机地址
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        self.sock.listen(5)
        # self.server_sock, self.saddr = self.sock.accept()   
    
    def settings(self, timeout):
        self.sock.settimeout(timeout)
    
    
    def listening(self):
        """
        :type server_socket: socket.socket
        :return 
        """
        while True:
            try:
                server_sock, self.saddr = self.sock.accept()
                data = server_sock.recv(2048)
                return (server_sock, data.decode())
            except TimeoutError:
                pass
    
    