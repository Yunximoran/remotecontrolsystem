import socket
import struct
import time

class UDPClient:
    def __init__(self, multicast_group, broadcast_address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))  # 绑定到任意可用地址和指定端口

        # 设置套接字选项以允许广播
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # 加入组播
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def send_unicast(self, message, address):
        self.sock.sendto(message.encode(), address)

    def send_broadcast(self, message):
        broadcast_addr = ('<broadcast>', 8000)  # 可以替换成你所需的广播地址
        self.sock.sendto(message.encode(), broadcast_addr)

    def send_multicast(self, message):
        multicast_addr = ('224.0.0.1', 8000)  # 组播地址和端口
        self.sock.sendto(message.encode(), multicast_addr)

    def receive(self):
        while True:
            data, addr = self.sock.recvfrom(1024)  # 接收数据
            print(f"Received message: {data.decode()} from {addr}")

if __name__ == "__main__":
    multicast_group = '224.0.0.1'  # 示例组播地址
    broadcast_address = '<broadcast>'  # 测试广播地址
    port = 8000

    client = UDPClient(multicast_group, broadcast_address, port)

    # 演示发送数据
    client.send_unicast("Hello Unicast", ('192.168.1.4', 9000))  # 替换成目标地址
    client.send_broadcast("Hello Broadcast")
    client.send_multicast("Hello Multicast")

    # 启动接收数据
    try:
        client.receive()
    except KeyboardInterrupt:
        client.sock.close()
