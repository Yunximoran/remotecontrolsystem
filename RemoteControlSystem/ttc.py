import socket

def tcp_client():
    # 创建一个 TCP 套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接到服务器 (IP 和端口)
        server_address = ('localhost', 12345)  # 替换为你的服务器地址和端口
        client_socket.connect(server_address)
        print("已连接到服务器")

        # 发送数据
        message = "你好，服务器！"
        client_socket.sendall(message.encode('utf-8'))
        print(f"发送: {message}")

        # 接收响应
        response = client_socket.recv(1024)  # 接收最多1024字节
        print(f"收到服务器消息: {response.decode('utf-8')}")

    except ConnectionRefusedError:
        print("连接被拒绝，请确保服务器正在运行并监听该端口。")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭套接字
        client_socket.close()
        print("连接已关闭")

if __name__ == "__main__":
    tcp_client()
