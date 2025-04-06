import re, socket
from pathlib import Path
from ._base import *
from lib import Resolver
from lib.sys.sock.tcp import Listener
resolver = Resolver()

PORT = resolver("ports", "tcp", "client")
ENCODING = resolver("global", "encoding")
OSLABEL = resolver("computer", "os")
logger = Logger("Select", log_file="select.log")

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
        # 启动TCP家庭
        print("Connect Serve Started")
        tcp_conn = Listener(
                (IP, PORT),
                listens=5,
                timeout=1,
                settings=[
                (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                ]
            )
        while True:
            try: 
                # 等待服务器发送shell指令            
                sock, _ = tcp_conn.accept()
                multiprocessing.Process(target=self.select, args=(sock,)).start()
            except TimeoutError:
                pass
            
            
    def select(self, sock:socket.socket):
        reports = []
        instructs = sock.recv(1024).decode()
        logger.record(1, f"recv instruct:{instructs}")
        
        for data in json.loads(instructs):
            # 解析指令模型
            item = json.loads(data)
            label = item['label']
            oslabel = item['os']
            instruct = item["instruct"]
            isadmin = item["isadmin"]
            kwargs = item['kwargs']
            
            # 指令分流，获取全部报文
            if oslabel == OSLABEL:
                report = self.executor_instruct(label, instruct, isadmin, kwargs)
            else:
                report= SYSTEM.report(instructs, f"{oslabel} instructions are not allowed to execute in {OSLABEL}", False)
                
            reports.append(report)
        self.report_results(sock, reports)
        

    def executor_instruct(self, label: str, instruct:str, isadmin:bool, kwargs:dict):
            # 指令分流
            if label == "close": # OK
                report = SYSTEM.close()
                
            elif label == "close -s":
                path = self.search_software(instruct)
                if path:
                    report = SYSTEM.close_software(path)
                else:
                    report = SYSTEM.report(instruct, False, "软件清单中没有加入这个软件")
                
            elif label == "restart": # OK
                report = SYSTEM.restart()
                
            elif label == "start -s":
                path = self.search_software(instruct)
                if path:
                    report = SYSTEM.start_software(path)
                else:
                    report = SYSTEM.report(instruct, False, "软件清单中没有加入这个软件")
                
            elif label == "wget":
                report = SYSTEM.wget()
                
            elif label == "compress":
                report = SYSTEM.compress()
                
            elif label == "uncompress":
                report = SYSTEM.uncompress()
                
            elif label == "remove":
                # 将instruct 处理成 topath
                report = SYSTEM.remove(instruct)
            else:
                report = SYSTEM.executor(instruct, isadmin=isadmin)
            return report
        
    def search_software(self, softname):
        with open(PATH_MAP_SOFTWARES, 'r', encoding="utf-8") as f:
            softwares = json.load(f)
            for soft in softwares:
                if softname == soft['ecdis']['name']:
                    pracpath = soft['ecdis']['prac-path']
                    return Path(pracpath)
        return False
    
                
    def savefile(self, filename, conn):
        fileobj = conn.recv(1024)
        conn.close()
        with open(os.path.join(LOCAL_DIR_FILE, filename), "wb") as f:
            f.write(fileobj)      
               
    def report_results(self, conn:socket.socket, reports:list):
        conn.sendall(json.dumps(reports, ensure_ascii=False, indent=4).encode(ENCODING))
        return reports     
    