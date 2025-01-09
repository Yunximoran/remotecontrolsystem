import platform
import socket
import uuid
from xml.etree import ElementTree as et

SYSTEM_NAME = platform.system()                 # 操作系统名称
SYSTEM_VERSION = platform.version()             # 操作系统版本
SYSTEM_ARCHITECTURE = platform.architecture()   # 操作系统位数
IP = socket.gethostbyname(socket.gethostname()) # IP地址
MAC = hex(uuid.getnode())  
XMLFILE = "config.xml"

class Init:
    def __init__(self):
        self.xmlroot = et.parse(XMLFILE)
        
        self.init()
    
    def init(self):
        self.baseConf = self.xmlroot.find('base')
        self.baseConf.set("ip", IP)
        self.baseConf.set("mac", MAC)
        self.xmlroot.write(XMLFILE)

Init()