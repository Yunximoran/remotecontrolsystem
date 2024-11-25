import multiprocessing
import time
import json

from databasetool import RedisConn as DATABASE
from core.tcp import TCP



LOCK = multiprocessing.Lock()
MESSAGEQUEUE = multiprocessing.Queue()


class Control:
    process = []
    CLIENTMESSAGE = {}
    
    def __init__(self):
        pass
    
    def push(self):
        pass
    
    def sendtoclient(self, shell_control:str, toclients=None):
        """
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
        if toclients is None or toclients is []:
            # 这里可能存在问题，我只需要
            toclients = [json.loads(client.decode())['ip'] for client in DATABASE.hgetall("heart_packages").values()]
            print(toclients)
        for client  in toclients:
            MESSAGEQUEUE.put(client)
            
        while MESSAGEQUEUE.qsize() > 0:
            p = multiprocessing.Process(target=self.sendtoshell, args=(shell_control, MESSAGEQUEUE.get()))
            p.start()
            p.join()
            
            
                
    def sendtoshell(self, shell_control, ip):
        conn = TCP()
        conn.send(shell_control, ip)
        conn.close()
