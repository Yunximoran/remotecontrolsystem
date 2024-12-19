import multiprocessing
import time
import json

from multiprocessing import Manager
from fastapi import websockets

from databasetool import RedisConn as DATABASE
from core.tcp import TCPConnect, TCPListen



LOCK = multiprocessing.Lock()
MESSAGEQUEUE = multiprocessing.Queue()
# WAITDONEQUEUE = Manager().Queue()


class Control:
    process = []
    CLIENTMESSAGE = {}
    
    def __init__(self):
        pass
    


    def listen(self):
        conn = TCPListen()
        pool = multiprocessing.Pool()
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
                pool.apply_async(self.waitdone, args=(sock, msg))   # 添加待办任务
            except:
                pass
    
    def waitdone(self, msg):
        DATABASE.lpush("waitdone_message", msg)
        # 阻塞函数，等待前端处理
        """
        前端通过接口返回处理结果，怎么找到对应的client套接字
        """

    
    
    def sendtoclient(self, shell_control:str, toclients = []):
        """
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
        print("hello wrold")
        if toclients == []:
            
            toclients = [client.decode() for client in DATABASE.hgetall("client_status").keys()]
            
        for client  in toclients:
            is_connect = DATABASE.hget("client_status", client).decode()
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


