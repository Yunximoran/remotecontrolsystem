# 客户端代码

import time
import subprocess
import multiprocessing
from typing import Annotated

from protocol import UDP, TCP


COMMUNICATION = multiprocessing.Queue()
SOFTWARTLIST = [] 


# udp_conn = UDP()
# tcp_conn = TCP()

class Client:
    ALLSERVER = []
    def __init__(self):
        self.start_connect_server()
        self.start_select_server()
        
        for p in self.ALLSERVER:
            p.join()
    

    def start_select_server(self):
        select_server = multiprocessing.Process(target=self.select, args=())
        select_server.start()
        self.ALLSERVER.append(select_server)
        
    
    def start_connect_server(self):
        connect_server = multiprocessing.Process(target=self.connect, args=())
        connect_server.start()
        self.ALLSERVER.append(connect_server)
        
    
    
    def run_shell(self, control: Annotated[list, None]):
        subprocess.Popen(control)
    
    
    def check_software(self):
        # 检查软件状态
        try:
            output = subprocess.check_output(['tasklist'], universal_newlines=True)  # 获取本机已启动进程池
            return [set(SOFTWARTLIST) - set(output)], set(SOFTWARTLIST) | set(output)   # 未启动列表， 已经启动列表
        except subprocess.CalledProcessError:
            return False
        
    
    def select(self):
        """
            监听tcp， 接受server发送的shell指令并启动
        """
        tcp_conn = TCP()
        # data = tcp_conn.listening()
        while True:
            data = tcp_conn.listening()
            
            
    
    def connect(self):
        # 每秒广播心跳包数据
        udp_conn = UDP()
        while True:
            time.sleep(1)
            # print("send a connection information to the server")
            udp_conn.send("id 000001 is connection 云曦墨染")
            
            


if __name__ == "__main__":
    Client()
"""
有个数据库，应该保存什么数据
"""
