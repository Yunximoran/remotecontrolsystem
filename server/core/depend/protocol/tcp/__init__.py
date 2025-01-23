import sys
import json
import multiprocessing

from .protype import TCP, socket
from databasetool import DataBaseManager as DATABASE
from projectdesposetool import CONFIG
from projectdesposetool.catchtools import Catch


class TCPConnect(TCP):
    
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def catchtimeout(func):
        def wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
                data = self.sock.recv(1024)
                return json.loads(data.decode('utf-8'))
            except ConnectionAbortedError:
                print("当前无连接")
            finally:
                self.sock.close()
        return wrapper
    
    @catchtimeout
    def send(self, ip, data):
        self.sock.connect((ip, CONFIG.TCPORT))
        self.sock.sendall(data.encode())
        

    @catchtimeout
    def sendfile(self, ip,file):
        self.sock.connect((ip, CONFIG.TCPORT))
        self.sock.sendall(file[0])
        self.sock.sendfile(file[1])
        
        
class TCPListen(TCP):
    def Init(self):
        self.sock.bind((CONFIG.IP, CONFIG.TSPORT))
        self.sock.listen(5)
    
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
    
    def recv(self):
        sock, addr = self.sock.accept()
        data = self.sock.recv(1024)
        return sock, addr, data.decode()
    
    @Catch.process
    def listen(self):
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
                sock, addr, data = self.recv()
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
                    pool.apply_async(self.add_watidone, args=(cookie, data,), 
                                    callback=lambda cookie: self.dps_waitdone(cookie, sock))           
                
                if msg['type'] == "report":
                    # 汇报事件
                    DATABASE.lpush("logs", data)
                    
            except TimeoutError:
                pass
            
    def add_watidone(self, cookie, msg):
        DATABASE.hset("waitdones", cookie, msg)
        """
        前端通过接口返回处理结果，怎么找到对应的client套接字
        """
        return cookie
        
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
            
