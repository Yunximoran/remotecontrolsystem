"""
需要保存的数据
    shell
    softwarelist
"""

# 客户端代码
import os
import json

from util import ListenServe, SelectServe, ConnectServe, BaseServe
from despose import CONFIG
from despose import build_directory

try:
    from system import SYSTEM
except ImportError as e:
    raise ImportError("系统未加载， 检查当前目录下是否存在system.py文件")

     
class Client:
    ALLSERVER: list[BaseServe] = [
        SelectServe(),
        ConnectServe(),
        ListenServe(),
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
        for serve in self.ALLSERVER:
            serve.process.start()
            
        for serve in self.ALLSERVER:
            serve.process.join()
        # self.__select_server()
        # self.__connect_server()
        # self.__listing_server()
        # self.__executor_server()
        
        # for server in self.ALLSERVER:
        #     server.join()
            
    # server
    # def __select_server(self):
    #     # 监听server并执行
    #     select_server = multiprocessing.Process(target=self.select, args=())
    #     select_server.start()
    #     self.ALLSERVER.append(select_server)
    
    # def __connect_server(self):
    #     # 保持连接状态
    #     connect_server = multiprocessing.Process(target=self.connect, args=())
    #     connect_server.start()
    #     self.ALLSERVER.append(connect_server)
    
    
    # def __listing_server(self):
    #     # 监听TCP，接受软件清单
    #     listen_server = multiprocessing.Process(target=self.listing_multi, args=())
    #     listen_server.start()
    #     self.ALLSERVER.append(listen_server)


    # # conning     
    # def select(self):
    #     """
    #         监听tcp  接受server发送的shell指令并启动

    #     shell指令应该包含
    #         操作类型
    #             compute close | restart
    #             software start | close
    #             other
    #         指令内容
            
    #     instruct = {
    #         "label: close | close -s,
    #         "instruct: "" | None
    #     }
    #     """
    #     tcp_conn =  TCPListen()
    #     while True:
    #         conn, data = tcp_conn.listening()
    #         if data:         
    #             instructs = json.loads(data)
    #             # tcp_conn.sendform("测试 tcp汇报服务器")
    #             with multiprocessing.Pool() as pool:
    #                 res_execute = pool.apply_async(self._execute_instruct, args=(instructs,),
    #                     callback=lambda report: self._report_results(conn, report))
    #                 res_history = pool.apply_async(self._history, args=(instructs,))
    #                 print("res", res_execute.get())
        
    # def _history(self, instructs):
    #     # 记录历史指令
    #     print("history process")
    #     with open(CONFIG.PATH_LOG_SHELLS, 'w', encoding="utf-8") as f:
    #         json.dump(instructs, f, ensure_ascii=False, indent=4)
                
    # def _report_results(self, conn, report:str):
    #     print(type(conn))
    #     conn.sendall(report.encode())
    #     conn.close()

    # def _execute_instruct(self, instructs:dict[str, str]):
    #     # 顺序执行shell
    #     print("execute process")
    #     label = instructs['name']   # label 标记指令用途
    #     shell = instructs['shell']  # shell 实习执行指令
        
    #     report = self.__instruct_default(label)
    #     if not report:
    #         report = self.__instruct_custom(shell)

    #     return json.dumps(report, ensure_ascii=False)

    # def __instruct_default(self, label):
    #     # 调用默认指令
    #     isdefault = True
    #     if label == "close":
    #         return SYSTEM.close()
    #     if label == "close -s":
    #         return  SYSTEM.close_software()
    #     if label == "restart":
    #         return SYSTEM.restart()
    #     if label == "start -s":
    #         return SYSTEM.start_software()
    #     if label == "wget":
    #         return SYSTEM.wget()
    #     if label == "compress":
    #         return SYSTEM.compress()
    #     if label == "uncompress":
    #         return SYSTEM.uncompress()
    #     return False
         
    # def __instruct_custom(self, instruct):
    #     # 调用自定义指令
    #     process = subprocess.Popen(instruct, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    #     msg, err = process.communicate()
    #     return {
    #         "status": "ok" if not err else "error",
    #         "instruct": instruct,
    #         "msg": msg if msg else "<No output>",
    #         "err": err if err else "<No error output>",
    #         "time": time.time()
    #     }
     
    # def listing_multi(self):
    #     # 组播接受软件清单
    #     # 在服务端获取更新 ？ 
    #     # 软件安装位置
    #     multi_conn = MultiCast()
    #     pool = multiprocessing.Pool()
    #     while True:
    #         data = multi_conn.recv()
    #         softwares = json.loads(data) # 解析服务端软件清单
    #         pool.apply_async(self._update_softwares, args=(softwares,), callback=self._write_local_softwares)
    
    # def connect(self):
    #     # 每秒广播心跳包数据
    #     udp_conn = BroadCast()
    #     while True:
    #         time.sleep(1)
    #         heart_pkgs = self.__get_heart_packages()
    #         udp_conn.send(json.dumps(heart_pkgs))
            
    # def _update_softwares(self, softwares):
    #     # 更新软件清单
    #     with open(CONFIG.PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
    #         local_softwares: list[dict] = (json.load(f))    # 加载本地软件清单
    #         for newitem in softwares:
    #             newsoftware = newitem['ecdis']['name']
    #             isexist = False
    #             for olditem in local_softwares: # 筛选重复项
    #                 oldsoftware = olditem['ecdis']['name']
    #                 if newsoftware == oldsoftware:
    #                     isexist = True
    #                     break
                    
    #             if not isexist: # 写入新对象
    #                 # 新的软件需要获取本地路径
    #                 # 动态处理 磁盘中查找所有匹配项，返回服务端，等待服务端处理
    #                 """
    #                 步骤
    #                     在local\softwares\中创建软连接[快捷方式]
                        
    #                 result: newitem['ecdis']['path'] = ./local/softwares/software.exe
    #                 """
    #                 allpath = SYSTEM.checkfile(newsoftware)
    #                 params = SYSTEM.format_params("choose software path", allpath)  # 格式化表单信息
    #                 res = SYSTEM.wait_response(params)
    #                 newitem['ecdis']['path'] = SYSTEM.build_softwarelink(res)
    #                 local_softwares.append(newitem)
                    
    #     return local_softwares
     
    # def _write_local_softwares(self, local_softwares):
    #     with open(CONFIG.PATH_MAP_SOFTWARES, "w", encoding='utf-8') as f:
    #         json.dump(local_softwares, f, ensure_ascii=False, indent=4)
    
    # def wait_respose(self, param):
    #     conn = TCPConnect()
    #     conn.send(param)
    #     return conn.recv()
    
    # def __get_heart_packages(self):
    #     with open(CONFIG.PATH_MAP_SOFTWARES, "r") as f:
    #         softwares = json.load(f)
    #         for item in softwares:
    #             try:    # 初始状态下item可能为None ? 历史问题， 后续可能不需要捕获异常
    #                 del item['ecdis']['path']
    #             except KeyError:
    #                 pass
    #     return {
    #         "mac": CONFIG.MAC,
    #         "ip": CONFIG.IP,
    #         "softwares": softwares
    #     }
        
            
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
