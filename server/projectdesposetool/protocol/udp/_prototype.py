import socket

class UDP:
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_DGRAM):
        self.sock = socket.socket(family, type)
        self._setting()
    
    def _setting(self):
        pass
    
    
    def close(self):
        self.sock.close