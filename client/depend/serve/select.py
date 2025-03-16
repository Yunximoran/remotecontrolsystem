import re, socket
from ._base import *
from depend.system import SYSTEM
from lib import Resolver

resolver = Resolver()
ENCODING = resolver("global", "encoding")


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
        tcp_conn =  TCPListen()
        # while True:
        #     sock, addr = tcp_conn.sock.accept()
            
        while True:
            try: 
                # 等待服务器发送shell指令            
                sock, _ = tcp_conn.accept()
                
                # 创建接受任务
                multiprocessing.Process(target=self.select, args=(sock,)).start()
            except TimeoutError:
                pass
            
    def select(self, sock:socket.socket):
        reports = []
        instructs = sock.recv(1024).decode()
        logger.record(1, f"recv instruct:{instructs}")
        for instruct in json.loads(instructs):
            
            item = json.loads(instruct)
            type = item['type']
            shell = item["shell"]
            isadmin = item["isadmin"]
            report = self.executor_instruct(type, shell, isadmin)
            reports.append(report)
            
            
        self.report_results(sock, reports)
        

    def executor_instruct(self, type, instruct, isadmin):
            # 指令分流
            if type == "close": # OK
                report = SYSTEM.close()
                
            elif type == "close -s":
                # instruct == software name
                report = SYSTEM.close_software(instruct)
                
            elif type == "restart": # OK
                report = SYSTEM.restart()
                
            elif type == "start -s":
                # instruct == software name
                report = SYSTEM.start_software(instruct)
                
            elif type == "wget":
                report = SYSTEM.wget()
                
            elif type == "compress":
                report = SYSTEM.compress()
                
            elif type == "uncompress":
                report = SYSTEM.uncompress()
                
            elif type == "remove":
                # 将instruct 处理成 topath
                report = SYSTEM.remove(instruct)
                
            else:
                report = SYSTEM.executor(instruct, isadmin=isadmin)
            return report
        
    def savefile(self, filename, conn):
        fileobj = conn.recv(1024)
        conn.close()
        with open(os.path.join(LOCAL_DIR_FILE, filename), "wb") as f:
            f.write(fileobj)      
               
    def report_results(self, conn:socket.socket, reports:list):
        conn.sendall(json.dumps(reports, ensure_ascii=False, indent=4).encode(ENCODING))
        return reports