import socket


class UDP:
    def __init__(self, address=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if address:
            self.sock.bind(address)
            
        self.settings()
        
    def settings(self):
        pass