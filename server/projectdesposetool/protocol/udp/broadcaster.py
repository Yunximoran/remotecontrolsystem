import socket
from ._prototype import UDP

class BroadCaster(UDP):
    
    def _setting(self):
        # 允许广播
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)