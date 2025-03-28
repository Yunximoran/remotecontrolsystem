try:
    import platform
    import psutil
    from lib.sys import NetWork
    from lib import Resolver
except ImportError:
    import os
    os.system(f"conda install --file requirements.txt")


if __name__ == "__main__":
    ip_server = input("请输入服务端地址:\t")
    netname = input("请输入网络适配器名称:\t")

    with Resolver() as resolver:
        net = resolver("network")
        computer = resolver("computer") 
        cpu = resolver("computer", "cpu")

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
        net.search("ip-server").settext(ip_server)
        
        # 初始化网络信息
        net_info = NetWork(netname)
        net.search("ip").settext(net_info.IPv4)
        net.search("mac").settext(net_info.mac)
