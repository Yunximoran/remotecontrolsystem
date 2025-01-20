import json
import time
import os
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
                print("Select Serve Recv:", data)
                try:
                    instruct = json.loads(data) # type: dict
                    print("exec instruct:", instruct)
                    with multiprocessing.Pool() as pool:
                        res_execute = pool.apply_async(self.execute_instruct, args=(instruct, ),
                            callback=lambda report: self.report_results(conn, report))
                        pool.apply_async(self.history, args=(instruct, ))
                        print(res_execute.get())
                except Exception:
                    print("exec download:", instruct)
                    multiprocessing.Process(self.savefile, args=(data, conn)).start()

                    
            except TimeoutError:
                pass
            
    def savefile(self, filename, conn):
        fileobj = conn.recv(1024)
        conn.close()
        with open(os.path.join(CONFIG.LOCAL_DIR_FILES, filename), "wb") as f:
            f.write(fileobj)
        
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
            report = SYSTEM.close()
            
        if label == "close -s":
            report = SYSTEM.close_software()
            
        if label == "restart":
            report = SYSTEM.restart()
            
        if label == "start -s":
            report = SYSTEM.start_software()
            
        if label == "wget":
            report = SYSTEM.wget(instruct)
            
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
            newitem = []
            with open(CONFIG.PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
                local_softwares: list[dict] = json.load(f)
                for item in softwares:
                    itemname = item['ecdis']['name']
                    isexist = False
                    for localitem in local_softwares:
                        localname = localitem['ecdis']['name']
                        if itemname == localname:
                            isexist = True
                            break
                    if not isexist:
                        newitem.append(item)
                
            pool.map_async(self._update_softwares, newitem, callback=self._write_local_softwares)
            
    def _update_softwares(self, softwares):
        # 更新软件清单
        software_name = softwares['ecdis']['name']
        print("software name", software_name)
        allpath = SYSTEM.checkfile(software_name)
        print("all path:", allpath)
        params = SYSTEM.format_params(1, allpath)
        resp = self._wait_response(params)
        print("results:", resp)
        softwares['ecdis']['path'], report = SYSTEM.build_hyperlink(software_name, resp)
        self._report_results(report)
        return softwares

     
    def _write_local_softwares(self, nvals):
        lcoal_softwares: list[dict]= json.load(open(CONFIG.PATH_MAP_SOFTWARES, 'r'))
        lcoal_softwares.extend(nvals)
        json.dump(lcoal_softwares, open(CONFIG.PATH_MAP_SOFTWARES, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        print("save ok")
            
    def _report_results(self, report):
        conn = TCPConnect()
        SYSTEM.format_params(2, report)
        conn.send(SYSTEM.format_params(2, report))
        conn.close()
        del conn
        
    def _wait_response(self, param):
        conn = TCPConnect()
        conn.send(param)
        data = conn.recv()
        conn.close()
        return data.decode()
