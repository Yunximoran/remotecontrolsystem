from socket import socket
from socket import error as SockError
from functools import wraps

class _CatchSock:
    socks = []
    def __init__(self):
        pass
    
    def sock(self, func):
        def wrapper(sock:socket, *args, **kwargs):
            try:
                sock.getpeername()
            except SockError:
                return False
            return func(*args, **kwargs)
        return wrapper
    