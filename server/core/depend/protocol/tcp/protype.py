import socket
from projectdesposetool import CONFIG



class TCP:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Init()
        self.settings()
    
    def Init(self):
        pass
    
    def settings(self):
        pass
    

