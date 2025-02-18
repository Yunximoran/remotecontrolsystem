import socket
from ._prototype import UDP

class MultiCaster(UDP):
    def _setting(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)