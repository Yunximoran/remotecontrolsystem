from ._base import *
from depend.system import SYSTEM



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
        while True:
            try: 
                # 等待服务器发送shell指令            
                conn, data = tcp_conn.recv()
                print("Select Serve Recv:", data)
                
                # 尝试使用json解释数据，如果无法解析则
                try:
                    # 解析TCP数据，转化成字典对象
                    instruct = json.loads(data) # type: dict
                    logger.record(1, f"exec instruct:{instruct}")
                    # 多进程启动
                    with multiprocessing.Pool() as pool:
                        res_execute = pool.apply_async(self.execute_instruct, args=(instruct, ),
                            callback=lambda report: self.report_results(conn, report))
                        pool.apply_async(self.history, args=(instruct, ))
                        print(res_execute.get())
                except Exception:
                    # 如果json解析异常，可能发送的是文件
                    # download 是向服务器文件下载至client
                    logger.record(1, f"exec download: {data}")
                    multiprocessing.Process(self.savefile, args=(data, conn)).start()
                    conn.close()
                    
            except TimeoutError:
                pass
            
    def savefile(self, filename, conn):
        fileobj = conn.recv(1024)
        conn.close()
        with open(os.path.join(LOCAL_DIR_FILE, filename), "wb") as f:
            f.write(fileobj)
        
    def history(self, instruct):
        # 记录历史指令
        print("history process")
        with open(PATH_LOG_SHELLS, 'w', encoding="utf-8") as f:
            json.dump(instruct, f, ensure_ascii=False, indent=4)
                
    def report_results(self, conn, report:str):
        conn.sendall(report.encode())
        conn.close()
        return report

    def execute_instruct(self, instruct:dict[str, str]):
        label = instruct['name']      # label 标记指令用途
        instruct = instruct['shell']  # shell 实际执行语句
        if label == "close": # OK
            report = SYSTEM.close()
            
        elif label == "close -s":
            # instruct == software name
            report = SYSTEM.close_software(instruct)
            
        elif label == "restart": # OK
            report = SYSTEM.restart()
            
        elif label == "start -s":
            # instruct == software name
            report = SYSTEM.start_software(instruct)
            
        elif label == "wget":
            report = SYSTEM.wget()
            
        elif label == "compress":
            report = SYSTEM.compress()
            
        elif label == "uncompress":
            report = SYSTEM.uncompress()
            
        else:
            report = SYSTEM.executor(instruct)
        return report
    
         
    