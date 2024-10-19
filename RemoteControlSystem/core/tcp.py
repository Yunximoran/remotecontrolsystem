import socket


from databasetool import RedisConn as DATABASE


SERVERADDRESS = ("192.168.179.1", 9091)    # 服务端TCP地址
CLIENTADDRESS = ("192.168.179.1", 8085)


class TCP:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.tcp_socket.bind(SERVERADDRESS)
        # self.tcp_socket.connect(CLIENTADDRESS)
        # self.tcp_socket.listen(5)
        
    
    def send(self, shell, client):
        # client_sock, client_address = self.tcp_socket.accept()
        
        # try:
        #     self.tcp_socket.connect(CLIENTADDRESS)      # clie
        # except:
        #     pass
        self.tcp_socket.connect(CLIENTADDRESS)
        self.tcp_socket.sendall(shell.encode())
        self.tcp_socket.close()
    
    def close(self):
        self.tcp_socket.close()
        
        """
        clientlist: client address
        
        client:
            mac: ***
            ip: ***
            port: ***
        """
        