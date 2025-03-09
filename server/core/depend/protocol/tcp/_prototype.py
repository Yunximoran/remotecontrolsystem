import socket



class TCP:
    def __init__(self, address=None, listens = 10):
        # 创建TCP套接字对象
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 初始化TCP套接字
        if address:
            self.sock.bind(address)
            self.sock.listen(listens)   # 默认监听10个连接
            
        self.settings()  # SOCK设置选项
        
    
    def settings(self):
        pass
