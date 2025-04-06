import sys
import argparse
try:
    import platform
    import psutil
    from lib.sys import NetWork
    from lib import Resolver
    
except ImportError:
    import os
    import sys
    os.system(f"conda create --file requirements.txt")
    sys.exit(0)

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--ip_server', help='设置服务端IPIP')
parser.add_argument('--broadcast', help='设置广播域')
parser.add_argument('--net', help="设置客户端网卡")
parser.add_argument("--username", help="计算机用户名称")
parser.add_argument("--password", help="计算机用户密码")
args = parser.parse_args()

IP_SERVER = args.ip_server    # 服务端地址
BROADCAST = args.broadcast    # 广播域名
NET = NetWork(args.net)       # 指定网卡
USERNAME = args.username
PASSWORD = args.password


if __name__ == "__main__":
    with Resolver() as resolver:
        net = resolver("network")
        computer = resolver("computer") 
        cpu = resolver("computer", "cpu")
        sock = resolver("sock")

        # 初始本机信息
        computer.setattrib("username", USERNAME)
        computer.setattrib("password", PASSWORD)
        computer.search("name").settext(platform.node())
        computer.search("os").settext(platform.system())
        computer.search("version").settext(platform.version())
        computer.search("machine").settext(platform.machine())
        computer.search("ram").settext(f"{psutil.virtual_memory().total / (1024 ** 3):.2f}")


        # 设置服务端IP
        net.search("ip-server").settext(IP_SERVER)
        
        # 初始化网络信息
        net.search("ip").settext(NET.IPv4)
        net.search("mac").settext(NET.mac)
        
        # 设置SOCK
        sock.search("ip-broad").settext(BROADCAST)
