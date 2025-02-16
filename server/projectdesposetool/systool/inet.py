import psutil
import struct
            
        
def choosenet(choose: str = None) -> dict:
    """
    choose: 指定工作网卡，None时返回所有网卡参数
    return: 返回网卡数据字典，key为网卡名称，value为包含IPv4/IPv6/MAC地址的字典
    """
    net_if_addrs = psutil.net_if_addrs()
    result = {}

    for interface_name, interface_addresses in net_if_addrs.items():
        if choose is None or choose == interface_name:
            net = {}
            for address in interface_addresses:
                if address.family.name.startswith('AF_INET6'):
                    net["IPv6"] = address.address
                elif address.family.name.startswith('AF_INET'):
                    net["IPv4"] = address.address
                elif address.family.name == 'AF_LINK':
                    net["mac"] = address.address
            result[interface_name] = net
            if choose is not None:  # 如果指定了网卡，直接返回
                return result[interface_name]
    
    return result

def formatmac(mac: str) -> str:
    # 格式化MAC地址，支持12位和17位格式
    if len(mac) == 12:
        pass
    if len(mac) == 17:
        if mac.count(":") == 5 or mac.count("-") == 5:
            sep = mac[2]
            mac = mac.replace(sep, '')
        else:
            raise ValueError("incorrect MAC format")
    else:
        raise ValueError("incorrect MAC format")
    
    return mac   

def create_magic_packet(mac) -> bytes:
    mac = formatmac(mac)
    data = b'FF' * 6 + (mac * 16).encode()
    send_data = b""
    for i in range(0, len(data), 2):
        send_data = send_data + struct.pack("B", int(data[i: i + 2], 16))
    return send_data


if __name__ == "__main__":
    nets = choosenet("WLAN")
    for net in nets:
        print(net)
        try:
            print(nets[net]["IPv4"])
            print(nets[net]['IPv6'])
            print(nets[net]['mac'])
        except TypeError:
            pass
