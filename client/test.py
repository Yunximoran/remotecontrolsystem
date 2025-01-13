import socket
import fcntl
import struct

def get_broadcast_address(interface='eth0'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 获取接口的IP地址和子网掩码
        ip = fcntl.ioctl(
            sock.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', interface.encode()[:15])
        )[20:24]
        netmask = fcntl.ioctl(
            sock.fileno(),
            0x891b,  # SIOCGIFNETMASK
            struct.pack('256s', interface.encode()[:15])
        )[20:24]
        
        # 计算广播地址
        broadcast = socket.inet_ntoa(struct.pack('4B', *(ip[i] | ~netmask[i] & 0xff for i in range(4))))
        return broadcast
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        sock.close()

# 示例：获取 eth0 接口的广播地址
broadcast_address = get_broadcast_address('eth0')
print(f"Broadcast Address: {broadcast_address}")
