"""
需要保存的数据
    shell
    softwarelist
"""

# 客户端代码
import os
import json
import multiprocessing

from depend import ListenServe, SelectServe, ConnectServe, BaseServe
from despose import CONFIG
from despose import build_directory
     
class Client:
    SERVES: list[multiprocessing.Process] = [
        multiprocessing.Process(target=SelectServe),
        multiprocessing.Process(target=ConnectServe),
        multiprocessing.Process(target=ListenServe)
    ]
    def __init__(self):
        self.build()
        self.start_server()
        
    def build(self):
        build_directory(CONFIG.LOCAL_DIR_DATA)
        build_directory(CONFIG.LOCAL_DIR_LOGS)
        build_directory(CONFIG.LOCAL_DIR_SOFTWARES)
   
        if not os.path.exists(CONFIG.PATH_MAP_SOFTWARES):
            print("make softwares.json file")
            with open(CONFIG.PATH_MAP_SOFTWARES, 'w', encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        if not os.path.exists(CONFIG.PATH_LOG_SHELLS):
            print("make shell.json file")
            with open(CONFIG.PATH_LOG_SHELLS, 'w', encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    
    def start_server(self):
        for serve in self.SERVES:
            serve.start()
    
            
        for serve in self.SERVES:
            serve.join()
            
if __name__ == "__main__":
    Client()
    
"""
软件位置应该在添加软件清单时配置
项目结构

data
local
    softwares
        software1
        software2
        software3
        software4
        。。。 软连接|快捷方式
        * 怎么导入 => 全盘扫描? 返回所有匹配项 => 汇报服务端，由服务端选择 | 客户端手动加入
        * 异常捕获：
            * 软件位置发生移动 => 软连接[快捷方式] 失效, 报告服务端， 重新建立连接[通知用户处理]
"""
