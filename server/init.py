import platform
from pathlib import Path
from xml.etree import ElementTree as ET

from dispose.sys.network import NetWork

SYSTEMNAME = platform.system()
SYSTEMVERSION = platform.version()
SYSTEMARCHITECTURE = platform.architecture()
# machine
SYSTEMMACHINE = platform.machine()
HOSTNAME = platform.node()  # 主机名称

NET = NetWork("WLAN")

WROKDIR = Path.cwd()
CONFFILE = WROKDIR.joinpath("config.xml")



def init():
    conf = ET.parse(CONFFILE)
    
    base = conf.find("base")
    base.set("ip", NET.IPv4)
    base.set("mac", NET.mac)
    
    conf.write(CONFFILE)
    
    
if __name__ =="__main__":
    # print(SYSTEMARCHITECTURE)
    # print(SYSTEMNAME)
    # print(SYSTEMVERSION)
    # print(SYSTEMMACHINE)
    # print(HOSTNAME)
    # print(platform.uname())
    print(platform.uname())
    uname = platform.uname()
    print(uname.version)
    print(uname.system)
    print(uname.node)
    print(uname.machine)