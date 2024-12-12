import json
import time
import subprocess
import multiprocessing

from despose import CONFIG, DESPOSE
from protocol import TCPListen, TCPConnect
from protocol import BroadCast, MultiCast
from .system import SYSTEM

class BaseServe:
    def __init__(self, *args, **kwargs):
        self.process = multiprocessing.Process(target=self.serve, args=args)
        # self.process.start()
    
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
            "label: close | close -s,
            "instruct: "" | None
        }
        """
        tcp_conn =  TCPListen()
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
        # 记录历史指令
        print("history process")
        with open(CONFIG.PATH_LOG_SHELLS, 'w', encoding="utf-8") as f:
            json.dump(instructs, f, ensure_ascii=False, indent=4)
                
    def _report_results(self, conn, report:str):
        print(type(conn))
        conn.sendall(report.encode())
        conn.close()

    def _execute_instruct(self, instructs:dict[str, str]):
        # 顺序执行shell
        print("execute process")
        label = instructs['name']   # label 标记指令用途
        shell = instructs['shell']  # shell 实习执行指令
        
        report = self.__instruct_default(label)
        if not report:
            report = self.__instruct_custom(shell)

        return json.dumps(report, ensure_ascii=False)

    def __instruct_default(self, label):
        # 调用默认指令
        isdefault = True
        if label == "close":
            return SYSTEM.close()
        if label == "close -s":
            return  SYSTEM.close_software()
        if label == "restart":
            return SYSTEM.restart()
        if label == "start -s":
            return SYSTEM.start_software()
        if label == "wget":
            return SYSTEM.wget()
        if label == "compress":
            return SYSTEM.compress()
        if label == "uncompress":
            return SYSTEM.uncompress()
        return False
         
    def __instruct_custom(self, instruct):
        # 调用自定义指令
        process = subprocess.Popen(instruct, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        msg, err = process.communicate()
        return {
            "status": "ok" if not err else "error",
            "instruct": instruct,
            "msg": msg if msg else "<No output>",
            "err": err if err else "<No error output>",
            "time": time.time()
        }
     
class ConnectServe(BaseServe):

    def serve(self):
        # 每秒广播心跳包数据
        udp_conn = BroadCast()
        while True:
            time.sleep(1)
            heart_pkgs = DESPOSE.get_heartpack()
            print(heart_pkgs)
            udp_conn.send(json.dumps(heart_pkgs))
            
   
        
class ListenServe(BaseServe):   
    def serve(self):
        # 组播接受软件清单
        # 在服务端获取更新 ？ 
        # 软件安装位置
        multi_conn = MultiCast()
        pool = multiprocessing.Pool()
        while True:
            data = multi_conn.recv()
            softwares = json.loads(data) # 解析服务端软件清单
            pool.apply_async(self._update_softwares, args=(softwares,), callback=self._write_local_softwares)
            
    def _update_softwares(self, softwares):
        # 更新软件清单
        with open(CONFIG.PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
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
                    # 新的软件需要获取本地路径
                    # 动态处理 磁盘中查找所有匹配项，返回服务端，等待服务端处理
                    """
                    步骤
                        在local\softwares\中创建软连接[快捷方式]
                        
                    result: newitem['ecdis']['path'] = ./local/softwares/software.exe
                    """
                    allpath = SYSTEM.checkfile(newsoftware)
                    params = SYSTEM.format_params("choose software path", allpath)  # 格式化表单信息
                    res = SYSTEM.wait_response(params)
                    newitem['ecdis']['path'] = SYSTEM.build_softwarelink(res)
                    local_softwares.append(newitem)
                    
        return local_softwares
     
    def _write_local_softwares(self, local_softwares):
        with open(CONFIG.PATH_MAP_SOFTWARES, "w", encoding='utf-8') as f:
            json.dump(local_softwares, f, ensure_ascii=False, indent=4)
    