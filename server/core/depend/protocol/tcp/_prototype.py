import socket
from projectdesposetool import CONFIG



class TCP:
    def __init__(self, address, listens = 5):
        # 创建TCP套接字对象
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.settings()  # SOCK设置选项
        
        # 初始化TCP套接字
        self.sock.bind(address)
        self.sock.listen(listens)   # 默认监听5个连接
        
        
    
    def settings(self):
        pass
