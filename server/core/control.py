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
        # multiprocessing.Process(target=self.listen)
        pass
    
    def push(self):
        pass

    def listen(self):
        conn = TCP()
        while True:
            try:
                data = conn.recv()
                print(data)
            except:
                pass
            
    
    def sendtoclient(self, shell_control:str, toclients = []):
        """
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
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
        conn = TCP()
        msg = conn.send(shell_control, ip)
        msg = json.loads(msg)
        print(msg)

            