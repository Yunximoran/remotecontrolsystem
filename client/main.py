"""
需要保存的数据
    shell
    softwarelist
"""

# 客户端代码
import os
import sys
from pathlib import Path
import time
import json
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
        # 启动Client服务
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
        
    def find_software(self, filename, search_path):
        for root, dirs, files in os.walk(search_path):
            if filename in files or search_path in dirs:
                print(f"找到文件{filename}")
                
                os.path.join(root, filename)
    def select(self):
        """
            监听tcp， 接受server发送的shell指令并启动
        """
        tcp_conn = TCP()
        while True:
            data = json.loads(tcp_conn.listening())
            with open("data.json", 'a', encoding="utf-8") as f:
                # for d in json.load(f):
                #     if d['label'] != data['label']:
                #         json.dump(data, f, ensure_ascii=False, indent=4)
                json.dump(data, f, ensure_ascii=False, indent=4)
                    # print("repeating data commit ignore")
            
            
    
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
