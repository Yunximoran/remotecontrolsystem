from socket import socket
from socket import error as SockError
from functools import wraps

from ._catch import _BaseCatch
from ..systools.logger import Logger


class _CatchSock(_BaseCatch):
    logger = Logger("sock", log_file="socket.log")
    socks = []
    def __init__(self):
        pass
    
    def sock(self, func):
        def wrapper(sock:socket, *args, **kwargs):
            try:
                sock.getpeername()
                self.record(func)
            except SockError as e:
                self.record(func, e, 3)
                return False
            return func(*args, **kwargs)
        return wrapper
    
    def checksockconning(self, func):
        """
            校验SOCK连接状态
        """
        def wrapper(sock:socket, *args, **kwargs):
            try:
                self.record(func)
                sock.getpeername()
            except SockError as e:
                self.record(func, e, 3)
                return e
            return func(*args, **kwargs)
        return wrapper