"""
需要保存的数据
    shell
    softwarelist
"""

# 客户端代码
import multiprocessing.managers
import os
import re
import socket
import time
import json
import subprocess
import multiprocessing
from multiprocessing.managers import BaseManager
from typing import Annotated

from protocol import BroadCast, TCP, MultiCast
from despose import CONFIG, checkfile

try:
    from system import SYSTEM
except ImportError as e:
    raise ImportError("系统未加载， 检查当前目录下是否存在system.py文件")

COMMUNICATION = multiprocessing.Queue()
INSTRUCTQUEUE = multiprocessing.Queue()
REPORTQUEUE = multiprocessing.Queue()
SOFTWARTLIST = [] 
SOFTWARE_PATH = ""



        
class Client:
    ALLSERVER: list[multiprocessing.Process] = []
    def __init__(self):
        self.build()
        self.start_server()
        
    def build(self):
        if not os.path.exists("data"):
            print("make data dir")
            os.mkdir("data")
            
        if not os.path.exists("data/softwares.json"):
            print("make softwares.json file")
            with open("data/softwares.json", 'w', encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        if not os.path.exists("data/shell.json"):
            print("make shell.json file")
            with open("data/shell.json", 'w', encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    
    def start_server(self):
        self.__select_server()
        self.__connect_server()
        self.__listing_server()
        # self.__executor_server()
        
        for server in self.ALLSERVER:
            server.join()
            
    # server
    def __select_server(self):
        # 监听server并执行
        select_server = multiprocessing.Process(target=self.select, args=())
        select_server.start()
        self.ALLSERVER.append(select_server)
    
    def __connect_server(self):
        # 保持连接状态
        connect_server = multiprocessing.Process(target=self.connect, args=())
        connect_server.start()
        self.ALLSERVER.append(connect_server)
    
    
    def __listing_server(self):
        # 监听TCP，接受软件清单
        listen_server = multiprocessing.Process(target=self.listing_multi, args=())
        listen_server.start()
        self.ALLSERVER.append(listen_server)
    
    
    def __executor_server(self):
        executor_server = multiprocessing.Process(target=self.executor, args=())
        executor_server.start()
        self.ALLSERVER.append(executor_server)
            
    
    # 接受消息后执行shell
    # shell报错是通知server处理
    """
    需要地址
    tcp
    """
    
    # conning     
    def select(self):
        """
            监听tcp  接受server发送的shell指令并启动

        shell指令应该包含
            操作类型
                compute close | restart
                software start | close
                other
            指令内容
            
        instruct = {
            "label: close | close -s,
            "instruct: "" | None
        }
        """
        tcp_conn =  TCP()
        while True:
            conn, data = tcp_conn.listening()
            if data:         
                instructs = json.loads(data)
                # tcp_conn.sendform("测试 tcp汇报服务器")
                with multiprocessing.Pool() as pool:
                    res_execute = pool.apply_async(self._execute_instruct, args=(instructs,),
                        callback=lambda report: self._report_results(conn, report))
                    res_history = pool.apply_async(self._history, args=(instructs,))
                    print("res", res_execute.get())

                    
                
                
    def _history(self, instructs):
        print("history process")
        with open("data/shell.json", 'w', encoding="utf-8") as f:
            json.dump(instructs, f, ensure_ascii=False, indent=4)
                
    def _report_results(self, conn, report:str):
        print(type(conn))
        conn.sendall(report.encode())
        conn.close()

    def _execute_instruct(self, instructs:dict[str, str]):
        # 顺序执行shell
        print("execute process")
        label = instructs['name']
        shell = instructs['shell']
        print(shell)
        process = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        msg, err = process.communicate()
        report = {
            "status": "ok" if not err else "error",
            "instruct": shell,
            "msg": msg if msg else "<No output>",
            "err": err if err else "<No error output>",
            "time": time.time()
        }

        return json.dumps(report, ensure_ascii=False)
            
    
            
    def listing_multi(self):
        # 组播接受软件清单
        # 在服务端获取更新 ？ 
        # 软件安装位置
        multi_conn = MultiCast()
        while True:
            data = multi_conn.recv()
            softwares = json.loads(data) # 解析服务端软件清单
            local_softwares = self.__update_softwares(softwares)    
            with open("data/softwares.json", "w", encoding='utf-8') as f:
                json.dump(local_softwares, f, ensure_ascii=False, indent=4)
                
                
    def connect(self):
        # 每秒广播心跳包数据
        udp_conn = BroadCast()
        while True:
            time.sleep(1)
            heart_pkgs = self.__get_heart_packages()
            udp_conn.send(json.dumps(heart_pkgs))
            
    def __update_softwares(self, softwares):
        # 更新软件清单
        with open('data/softwares.json', 'r', encoding='utf-8') as f:
            local_softwares: list[dict] = (json.load(f))    # 加载本地软件清单
            for newitem in softwares:
                newsoftware = newitem['ecdis']['name']
                isexist = False
                for olditem in local_softwares: # 筛选重复项
                    oldsoftware = olditem['ecdis']['name']
                    if newsoftware == oldsoftware:
                        isexist = True
                        break
                    
                if not isexist: # 写入新对象
                    software_path = checkfile(newsoftware, SOFTWARE_PATH)
                    newitem['ecdis']['path'] = softwares  # 更新软件安装路径  * 可能为None
                    if software_path is None:
                        pass    # 如果软件不存在则需要通知服务端处理
                    
                    # 不管软件是否安装，都写入软件清单
                    local_softwares.append(newitem)
        return local_softwares
    
    
    def __get_heart_packages(self):
        with open("data/softwares.json", "r") as f:
            softwares = json.load(f)
            for item in softwares:
                try:    # 初始状态下item可能为None ? 历史问题， 后续可能不需要捕获异常
                    del item['ecdis']['path']
                except KeyError:
                    pass
        return {
            "mac": CONFIG.MAC,
            "ip": CONFIG.IP,
            "softwares": softwares
        }
        
    def __find_software(self, software):
        for root, dirs, files in os.walk(SOFTWARE_PATH):
            if software in files:
                return None
            
    def executor(self):
        tcp_conn = TCP(port=8088)
        while True:
            instruct = COMMUNICATION.get()
            tcp_conn.sendform(instruct)
            
def logo():
    while True:
        time.sleep(1)
        print("Hello world")

if __name__ == "__main__":
    Client()
    # with BaseManager() as PROCESSMANAGER:
    #     PROCESSMANAGER.register("tcp_conn", TCP)
    #     Client(PROCESSMANAGER)
    
"""
软件位置应该在添加软件清单时配置

"""
