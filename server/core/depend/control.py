import multiprocessing
import socket

from databasetool import DataBaseManager as DATABASE
from core.depend.protocol.tcp import TCPConnect



LOCK = multiprocessing.Lock()
MESSAGEQUEUE = multiprocessing.Queue()
WAITDONEQUEUE = multiprocessing.Queue()


class Control:
    process = []
    waittasks: dict[str, socket.socket] = {}
    
    def __init__(self):
        pass
            
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