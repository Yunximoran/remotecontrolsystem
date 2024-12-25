import json
import time
import subprocess
import multiprocessing

from despose import CONFIG, DESPOSE
from .protocol import TCPListen, TCPConnect
from .protocol import BroadCast, MultiCast

try:
    from .system import SYSTEM
except ImportError:
    pass
    # raise ImportError("导入失败，请检查depend\system.py 是否存在")


class BaseServe:
    def __init__(self):
        self.serve()
    
    def serve(self):
        pass

class SelectServe(BaseServe):

    def serve(self):
        """
            监听tcp  接受server发送的shell指令并启动

        shell指令应该包含
            操作类型
                compute close | restart
                software start | close
                other
            指令内容
            
        instruct = {
            "label: close | close -s,   # 应该更具体一点 ？ 但麻烦的就是服务端的处理， 需要保存pid的进程应该只有启动软件 是这样吗？
            "instruct: "" | None
        }
        """
        tcp_conn =  TCPListen()
        while True:
            try:             
                conn, data = tcp_conn.recv()
                instruct = json.loads(data) # type: dict
                # # 某个参数不可被序列化, 使用pool会报错，但是使用process则不会
                # 怎么解决pool运行时不可被序列化的问题
                with multiprocessing.Pool() as pool:
                    res_execute = pool.apply_async(self.execute_instruct, args=(instruct, ),
                        callback=lambda report: self.report_results(conn, report))
                    res_history = pool.apply_async(self.history, args=(instruct, ))
                    print(res_execute.get())
            except TimeoutError:
                pass
            

        
    def history(self, instruct):
        # 记录历史指令
        print("history process")
        with open(CONFIG.PATH_LOG_SHELLS, 'w', encoding="utf-8") as f:
            json.dump(instruct, f, ensure_ascii=False, indent=4)
                
    def report_results(self, conn, report:str):
        conn.sendall(report.encode())
        conn.close()
        return report

    def execute_instruct(self, instruct:dict[str, str]):
        label = instruct['name']      # label 标记指令用途
        instruct = instruct['shell'] # shell 实际执行语句
        if label == "close":
            report =  SYSTEM.close()
            
        if label == "close -s":
            report =   SYSTEM.close_software()
            
        if label == "restart":
            report =  SYSTEM.restart()
            
        if label == "start -s":
            report = SYSTEM.start_software()
            
        if label == "wget":
            report = SYSTEM.wget()
            
        if label == "compress":
            report = SYSTEM.compress()
            
        if label == "uncompress":
            report = SYSTEM.uncompress()
        
        report = SYSTEM.executor(instruct)
        return report
    
         
    

     
class ConnectServe(BaseServe):

    def serve(self):
        # 每秒广播心跳包数据
        udp_conn = BroadCast()
        while True:
            time.sleep(1)
            heart_pkgs = DESPOSE.get_heartpack()
            # print(heart_pkgs)
            udp_conn.send(json.dumps(heart_pkgs))   
        
class ListenServe(BaseServe): 
    # 监听组播端口， 获取软件清单  
    def serve(self):
        multi_conn = MultiCast()    # 激活组播端口
        pool = multiprocessing.Pool()
        while True:
            data = multi_conn.recv()
            softwares = json.loads(data) # 解析服务端软件清单
            # pool.map_async(self._update_softwares, softwares)
            # 为每次接收到的软件清单创建处理进程
            print(softwares)
            pool.apply_async(self._update_softwares, args=(softwares,), callback=self._write_local_softwares)
            
    def _update_softwares(self, softwares):
        # 更新软件清单
        with open(CONFIG.PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
            local_softwares: list[dict] = (json.load(f))    # 加载本地软件清单
            for newitem in softwares:
                # 遍历软件清单
                newsoftware = newitem['ecdis']['name']
                isexist = False
                for olditem in local_softwares: # 筛选重复项
                    oldsoftware = olditem['ecdis']['name']
                    if newsoftware == oldsoftware:
                        isexist = True
                        break
                    
                if not isexist: # 写入新对象
                    # 新的软件需要获取本地路径
                    # 动态处理 磁盘中查找所有匹配项，返回服务端，等待服务端处理
                    """
                    步骤
                        在local\softwares\中创建软连接[符号链接]
                        
                    result: newitem['ecdis']['path'] = ./local/softwares/software.exe
                    """
                    allpath = SYSTEM.checkfile(newsoftware) # 在磁盘总搜索所有包含软件名的路径
                    print(allpath)
                    params = SYSTEM.format_params(1, allpath)  # 格式化表单信息
                    res = self._wait_response(params)  # 等待服务器选择正确路径
                    print("respath", res)
                    newitem['ecdis']['path'], report = SYSTEM.build_hyperlink(newsoftware, res)
                    self._report_results(report)
                    
                    local_softwares.append(newitem)
                    
        return local_softwares
     
    def _write_local_softwares(self, local_softwares):
        with open(CONFIG.PATH_MAP_SOFTWARES, "w", encoding='utf-8') as f:
            json.dump(local_softwares, f, ensure_ascii=False, indent=4)
            
    def _report_results(self, report):
        conn = TCPConnect()
        conn.send(report)
        conn.close()
        del conn
        
    def _wait_response(self, param):
        conn = TCPConnect()
        conn.send(json.dumps(param, ensure_ascii=False))
        data = conn.recv(1024)
        conn.close()
        return data.decode()

    def add_pathfield(self, item):
        pass

