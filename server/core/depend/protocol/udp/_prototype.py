import socket


class UDP:
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.settings()
        self.sock.bind(address)
    
    def settings():
        pass