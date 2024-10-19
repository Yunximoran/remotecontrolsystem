import platform
import socket
import uuid


SYSTEM_NAME = platform.system()                 # 操作系统名称
SYSTEM_VERSION = platform.version()             # 操作系统版本
SYSTEM_ARCHITECTURE = platform.architecture()   # 操作系统位数
IP = socket.gethostbyname(socket.gethostname()) # IP地址
MAC = hex(uuid.getnode())                       # MAC地址
SOFTWARE = []


class Init:
    """
        初始化项目
    """
    def __init__(self):
        pass


if SYSTEM_NAME == "window":
    pass

elif SYSTEM_NAME == "linux":
    pass

elif SYSTEM_NAME == "macOS":
    pass