"""
    初始化配置文件

检测操作系统
选择物理网卡
"""

import platform
import pathlib
import uuid
from xml.etree import ElementTree as et

from projectdesposetool.systools import NetWork


NET = NetWork("WLAN")
SYSTEM_NAME = platform.system()                 # 操作系统名称
SYSTEM_VERSION = platform.version()             # 操作系统版本
SYSTEM_ARCHITECTURE = platform.architecture()   # 操作系统位数
IP = NET.IPv4
MAC = NET.mac
XMLFILE = "config.xml"
WORKDIR = pathlib.Path.cwd()

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