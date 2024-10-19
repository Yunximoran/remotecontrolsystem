import socket
import uuid

def get_ip_address():
    """获取本机的IP地址"""
    hostname = socket.gethostname()  # 获取本机的主机名
    ip_address = socket.gethostbyname(hostname)  # 获取主机名对应的IP地址
    return ip_address

def get_mac_address():
    """获取本机的MAC地址"""
    mac = hex(uuid.getnode())[2:]  # 获取MAC地址并转换为十六进制格式
    mac_address = ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])  # 格式化
    return mac_address

if __name__ == "__main__":
    ip_address = get_ip_address()
    mac_address = get_mac_address()
    
    print(f"本机IP地址: {ip_address}")
    print(f"本机MAC地址: {mac_address}")
