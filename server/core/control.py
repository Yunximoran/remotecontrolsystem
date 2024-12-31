import multiprocessing
import socket
import json

from multiprocessing import Manager
from fastapi import websockets

from databasetool import DataBaseManager as DATABASE
from core.tcp import TCPConnect, TCPListen



LOCK = multiprocessing.Lock()
MESSAGEQUEUE = multiprocessing.Queue()
WAITDONEQUEUE = multiprocessing.Queue()


class Control:
    process = []
    waittasks: dict[str, socket.socket] = {}
    
    def __init__(self):
        pass
    


    def listen(self):
        conn = TCPListen()
        pool = multiprocessing.Pool()
        try:
            while True:
                try:
                    # 监听待办事件
                    """
                    写入redis 供vue读取
                    等待vue执行处理
                    
                    * 更新待办事件
                    * 创建处理任务
                        pass
                    """
                    sock, addr, data = conn.recv()
                    """
                    cookie: (typecode + ip + ctime).encode()
                    """
                    msg = json.loads(data)
                    cookie = msg['cookie']
                    if msg['type'] == "instruct":
                        # 指令事件
                        pass
                    
                    if msg['type'] == "software":
                        # 软件事件
                        pool.apply_async(self.add_watidone, args=(cookie, data,), callback=lambda cookie: self.dps_waitdone(cookie, sock))
                                        
                    
                    if msg['type'] == "report":
                        # 汇报事件
                        DATABASE.lpush("logs", data)
                    

                except TimeoutError:
                    print("TCP Listen Timeout")
        except KeyboardInterrupt as e:
            print(e)
    
    def add_watidone(self, cookie, msg):
        DATABASE.lset("waitdones", cookie, msg)
        """
        前端通过接口返回处理结果，怎么找到对应的client套接字
        """
        return cookie
    
    def add_reports(self, cookie, msg):
        pass
        
    def dps_waitdone(self, cookie, sock:socket.socket):
        while True:
            
            try:
                sock.getpeername()
            except socket.error:
                print("client disconnected")
                break
            
            result:str = DATABASE.hget('waitdone_despose_results', cookie)
            if result:
                sock.sendall(result.encode())
                sock.close()
                break
            
            
        
        """
        
        results: igonre
        results: shelllist{
            
        }
        """
    
    def sendtoclient(self, shell_control:str, toclients = []):
        """
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
        print("hello wrold")
        if toclients == []:
            
            toclients = [client for client in DATABASE.hgetall("client_status").keys()]
            
        for client  in toclients:
            is_connect = DATABASE.hget("client_status", client)
            if is_connect == "true":
                MESSAGEQUEUE.put(client)
            
        while MESSAGEQUEUE.qsize() > 0:
            p = multiprocessing.Process(target=self.sendtoshell, args=(shell_control, MESSAGEQUEUE.get()))
            p.start()
            p.join()
            
    
                
    def sendtoshell(self, shell_control, ip):
        """
            一次只发送一个指令，
        """
        conn = TCPConnect() 
        report = conn.send(shell_control, ip)
        DATABASE.lset("reports", ip, report)
        DATABASE.lpush("logs", report)

controlor = Control()