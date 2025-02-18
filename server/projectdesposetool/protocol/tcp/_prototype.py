import socket

class TCP:
    def __init__(self, fimaly=socket.AF_INET, type=socket.SOCK_STREAM):
        self.sock = socket.socket(fimaly, type)
        self.init()
        self.setting()
        
    def init(self):
        pass
    def setting(self):
        pass
    
    def close(self):
        self.sock.close()