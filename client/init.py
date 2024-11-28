import platform
import socket
import uuid
from xml.etree import ElementTree as et


SYSTEM_NAME = platform.system()                 # 操作系统名称
SYSTEM_VERSION = platform.version()             # 操作系统版本
SYSTEM_ARCHITECTURE = platform.architecture()   # 操作系统位数
IP = socket.gethostbyname(socket.gethostname()) # IP地址
MAC = hex(uuid.getnode())                       # MAC地址



    
class Init:
    """
        初始化项目
    """
    
    
    def __init__(self):
        self.system = self.load_system()
        self.init()

    def init(self):
        self.__init_local_address() # 初始化本地IP、MAC
        
    def __init_local_address(self):
        tree = et.parse("config.xml")
        root = tree.getroot()
        print(IP)
        root.set("ip", IP)
        root.set("mac", MAC)
        tree.write("config.xml")
    
    def load_system(self):
        if SYSTEM_NAME == "Windows":
            return WindowSystem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)

        elif SYSTEM_NAME == "Linux":
            return LinuxSystem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)

        elif SYSTEM_NAME == "macOS":
            return MacOSSytem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
        
        else:
            return BaseSystem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
        
        
        
class BaseSystem:
    def __init__(self, version, architecure):
        self.version = version
        self.bit, self.linktype = architecure
    
class WindowSystem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)

class LinuxSystem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        
class MacOSSytem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        
        
        
if __name__ == "__main__":
    Init()
