import multiprocessing
import time
import json

from databasetool import RedisConn as DATABASE
from core.tcp import TCP



LOCK = multiprocessing.Lock()
MESSAGEQUEUE = multiprocessing.Queue()


class Control:
    CLIENTMESSAGE = {}
    
    def __init__(self):
        pass
    
    def push(self):
        pass
    
    def sendtoclient(self, shell_control:str):
        """
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
        for client  in DATABASE.hgetall("heart_packages").values():
            info = json.loads(client.decode())
            MESSAGEQUEUE.put(info['ip'])
            
        while MESSAGEQUEUE.qsize() > 0:
            print(shell_control)
            p = multiprocessing.Process(target=self.sendtoshell, args=(shell_control, MESSAGEQUEUE.get()))
            p.start()
            p.join()
            
                
    def sendtoshell(self, shell_control, ip):
        conn = TCP()
        print(ip)
        conn.send(shell_control, ip)
        conn.close()
