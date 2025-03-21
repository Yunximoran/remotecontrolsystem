# 客户端代码
import json
import multiprocessing

from depend.serve import ListenServe, SelectServe, ConnectServe
from depend.path import *

class Client:
    # 注册服务
    servers: list[multiprocessing.Process] = [
        multiprocessing.Process(target=SelectServe),    # 选中并执行服务： 接受instuct，并执行
        multiprocessing.Process(target=ConnectServe),   # 连接服务： 连接服务端，定期发送软件清单
        multiprocessing.Process(target=ListenServe),    # 监听服务： 接受服务端，处理待办事件
    ]
    def __init__(self):
        print("client runing")
        self.build()
        self.start_server()
        
    def build(self):
        if not LOCAL_DIR_DATA.exists():
            LOCAL_DIR_DATA.mkdir(parents=True)
        
        if not LOCAL_DIR_LOGS.exists():
            LOCAL_DIR_LOGS.mkdir(parents=True)
            
        if not LOCAL_DIR_SOFT.exists():
            LOCAL_DIR_SOFT.mkdir(parents=True)
            
        if not LOCAL_DIR_FILE.exists():
            LOCAL_DIR_FILE.mkdir(parents=True)
   
        if not PATH_MAP_SOFTWARES.exists():
            # 创建软件清单文件
            print("make softwares.json file")
            with open(PATH_MAP_SOFTWARES, 'w', encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        if not PATH_LOG_SHELLS.exists():
            # 创建shell文件，保存历史shell
            print("make shell.json file")
            with open(PATH_LOG_SHELLS, 'w', encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    
    def start_server(self):
        # 启动服务
        for serve in self.servers:
            serve.start()

        for serve in self.servers:
            serve.join()
            
if __name__ == "__main__":
    Client()