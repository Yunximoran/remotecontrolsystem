import re, socket
from pathlib import Path
from ._base import *
from lib import Resolver
from lib.sys.sock.tcp import Listener, Connector
resolver = Resolver()

PORT = resolver("ports", "tcp", "client")
FILEPORT = resolver("ports", "tcp", "client-file")
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
                report = self.executor_instruct(sock, label, instruct, isadmin, kwargs)
            else:
                report= SYSTEM.report(instructs, f"{oslabel} instructions are not allowed to execute in {OSLABEL}", False)
                
            reports.append(report)
        self.report_results(sock, reports)

    def executor_instruct(
        self, 
        sock:socket.socket,
        label: str,
        instruct:str, 
        isadmin:bool,
        kwargs:dict):   # 指令分流
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
                
            elif label == "download":
                sock.sendall("OK".encode(ENCODING))
                filename = self.recvfile()
                report = SYSTEM.report(
                    [label, filename],
                    "OK",
                    False
                )
            elif label == "remove":
                # 将instruct 处理成 topath
                report = SYSTEM.remove(instruct)
            else:
                report = SYSTEM.executor(instruct, isadmin=isadmin)
            return report
    
    def recvfile(self):
        # 创建文件接收通道
        file_conn = Listener(
            (IP, FILEPORT),
            listens=5
        )
        conn, _ = file_conn.accept()
        filenum = conn.recv(1024).decode(ENCODING)   # 接收的文件数量
        for _ in range(int(filenum)):
            filename = conn.recv(1024).decode(ENCODING) # 接收文件名称
            filesize = conn.recv(1024).decode(ENCODING) # 接收文件大小
            
            # 开始接收文件
            size = 0
            with open(LOCAL_DIR_FILE.joinpath(filename), 'wb') as f:
                while size < int(filesize):
                    data = conn.recv(4096)
                    f.write(data) 
                    size += len(data)
                    print(f"{size} - > {filesize}")
            # 通知服务端当前文件接收文件完毕，可以发送下一个文件
            conn.sendall(f"recv: {filename} OK".encode())
        return filename
    def search_software(self, softname):
        with open(PATH_MAP_SOFTWARES, 'r', encoding="utf-8") as f:
            softwares = json.load(f)
            for soft in softwares:
                if softname == soft['ecdis']['name']:
                    pracpath = soft['ecdis']['prac-path']
                    return Path(pracpath)
        return False
               
    def report_results(self, conn:socket.socket, reports:list):
        conn.sendall(json.dumps(reports, ensure_ascii=False, indent=4).encode(ENCODING))
        return reports     
    