"""
需要保存的数据
    shell
    softwarelist
"""

# 客户端代码
import os
import time
import json
import subprocess
import multiprocessing
from typing import Annotated

from protocol import BroadCast, TCP, MultiCast
from despose import CONFIG, load_software

COMMUNICATION = multiprocessing.Queue()
SOFTWARTLIST = [] 


# udp_conn = UDP()
# tcp_conn = TCP()

class Client:
    ALLSERVER: list[multiprocessing.Process] = []
    def __init__(self):
        # 启动Client服务
        self.start_connect_server()
        self.start_select_server()
        self.start_listing_server()
        
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
    
    
    def start_listing_server(self):
        listen_server = multiprocessing.Process(target=self.listing_multi, args=())
        listen_server.start()
        self.ALLSERVER.append(listen_server)
    
    
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
            with open("data/shell.json", 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    
            
    def listing_multi(self):
        multi_conn = MultiCast()
        while True:
            data = multi_conn.recv()
            soft_list = json.loads(data)
            print(soft_list)
            with open('data/softwares.json', 'w', encoding='utf-8') as f:
                json.dump(soft_list, f, ensure_ascii=False, indent=4)
                
    def connect(self):
        # 每秒广播心跳包数据
        udp_conn = BroadCast()
        while True:
            time.sleep(1)
            heart_pkgs = self.get_heart_packages()
            udp_conn.send(json.dumps(heart_pkgs))
            
    def get_heart_packages(self):
        """
        software: {
            ecdis{
                name: version
            }
        }
        """
        return {
            "mac": CONFIG.MAC,
            "ip": CONFIG.IP,
            "software": load_software()
        }
            


if __name__ == "__main__":
    Client()
    
"""
有个数据库，应该保存什么数据
"""
