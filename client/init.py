try:
    import platform
    import psutil
    from lib.sys import NetWork
    from lib import Resolver
except ImportError:
    import os
    import sys
    os.system(f"conda install --file requirements.txt")
    sys.exit(0)
    
IP_SERVER = "192.168.31.176"    # 服务端地址
BROADCAST = "192.168.31.255"    # 广播域名
NET =  NetWork("WLAN")          # 指定网卡


if __name__ == "__main__":
    with Resolver() as resolver:
        net = resolver("network")
        computer = resolver("computer") 
        cpu = resolver("computer", "cpu")
        sock = resolver("sock")

        # 初始本机信息
        computer.search("name").settext(platform.node())
        computer.search("os").settext(platform.system())
        computer.search("version").settext(platform.version())
        computer.search("machine").settext(platform.machine())
        computer.search("ram").settext(f"{psutil.virtual_memory().total / (1024 ** 3):.2f}")

        # 初始化CPU信息
        cpu.search("processor").settext(platform.processor())
        cpu.search("physical-cores").settext(psutil.cpu_count(logical=False))
        cpu.search("logical-cores").settext(psutil.cpu_count(logical=True))
        cpu.search("architecture").settext(platform.architecture()[0])

        # 设置服务端IP
        net.search("ip-server").settext(IP_SERVER)
        
        # 初始化网络信息
        net.search("ip").settext(NET.IPv4)
        net.search("mac").settext(NET.mac)
        
        # 设置SOCK
        sock.search("ip-broad").settext(BROADCAST)
