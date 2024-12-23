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
                sock, msg = conn.recv()
                self.add_watidone(sock, msg)
                # pool.apply_async(self.add_watidone, args=(sock, msg))   # 添加待办任务
            except TimeoutError:
                pass
    
    def add_watidone(self, sock, msg):
        self.waittasks[msg] = sock
        DATABASE.hset("waitdones", msg, "false")
        """
        前端通过接口返回处理结果，怎么找到对应的client套接字
        """
        
    def dps_waitdone(self, msg, response: str):
        sock = self.waittasks[msg]
        sock.sendall(response.encode())
        sock.close()
        DATABASE.hdel("waitdones", msg)
        del sock
        del self.waittasks[msg]
        
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
        DATABASE.lpush("reports", report)
        DATABASE.hset("logs", ip, report)



if __name__ == "__main__":
    Control().listen()
