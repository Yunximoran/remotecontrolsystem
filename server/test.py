import psutil


# 获取所有网络接口信息
net_if_addrs = psutil.net_if_addrs()

# 遍历每个网络接口
for interface_name, interface_addresses in net_if_addrs.items():
    print(f"网卡名称: {interface_name}")
    for address in interface_addresses:
        if address.family.name.startswith('AF_INET'):
            print(f"  IPv4 地址: {address.address}")
        elif address.family.name.startswith('AF_INET6'):
            print(f"  IPv6 地址: {address.address}")
        elif address.family.name == 'AF_LINK':
            print(f"  MAC 地址: {address.address}")
            
    for address in interface_addresses:
        print(address)