import psutil
import time

def get_network_speed(interface='eth0', interval=1):
    # 获取初始网络统计信息
    stats_before = psutil.net_io_counters(pernic=True).get(interface)
    bytes_before = stats_before.bytes_sent + stats_before.bytes_recv

    # 等待一段时间
    time.sleep(interval)

    # 获取新的统计信息
    stats_after = psutil.net_io_counters(pernic=True).get(interface)
    bytes_after = stats_after.bytes_sent + stats_after.bytes_recv

    # 计算速率（字节/秒 → Mbps）
    bytes_per_sec = (bytes_after - bytes_before) / interval
    mbps = bytes_per_sec * 8 / (1024 ** 2)  # 1 byte = 8 bits, 1 Mbps = 1024^2 bits/s
    return (round(mbps, 3))

# 示例：监控默认接口（需替换为你的网络接口名，如 'eth0'、'en0'、'Wi-Fi'）
interface = 'WLAN'  # Windows 可能是 '以太网'，Linux 可能是 'eth0'，Mac 可能是 'en0'
speed = get_network_speed(interface)
print(f"当前带宽使用: {speed:.2f} Mbps")