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
        [MESSAGEQUEUE.put(client.decode()) for client in DATABASE.hgetall("client_message")]

        while MESSAGEQUEUE.qsize() > 0:
            print(shell_control)
            p = multiprocessing.Process(target=self.connect_client, args=(shell_control, MESSAGEQUEUE.get()))
            p.start()
            p.join()
            
                
    def connect_client(self, shell_control, client):
        conn = TCP()
        conn.send(shell_control, client)
        conn.close()
