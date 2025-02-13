import json

from .protype import TCP, socket
from databasetool import DataBaseManager as DATABASE
from projectdesposetool import CONFIG
from projectdesposetool.catchtools import Catch
from projectdesposetool.systool.custprocess import MultiProcess


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
    
    @Catch.timeout
    def recv(self):
        sock, addr = self.sock.accept()
        data = self.sock.recv(1024)
        return sock, addr, data.decode()

        
    def _parse(data):
        """
            解析TCP数据
        返回事件类型和Cookie
        """
        msg = json.loads(data)
        event_type = msg['type']
        cookie = msg['cookie']
        return event_type, cookie

    def _event_brench(self, t, cookie, data, sock):
        """
            事件分支
        区分不同类型事件，执行对应事件
        """
        if t == "instruct":
            pass
                
        if t == "software":
            """
                软件事件
            """
            self.add_watidone(cookie, data)
            self.dps_waitdone(cookie, sock)          
                
        if t == "report":
            """
                获取汇报结果
            客户端控制指令执行结果返回服务端
            服务端保存至redis数据库
            yumo
            """
            DATABASE.lpush("logs", data)

    def listen(self):
        while True:
            conn = self.recv()
            if conn:
                MultiProcess(target=self._listen, args=(conn, )).start()

    def _listen(self, conn):
        # ???
        sock, addr, data = conn
        event_type, cookie = self._parse(data)
        self._event_brench(event_type, cookie, data, sock)

                      
    def add_watidone(self, cookie, msg):
        DATABASE.hset("waitdones", cookie, msg)
        """
        前端通过接口返回处理结果，怎么找到对应的client套接字
        """
        return cookie
    
    @Catch.sock
    def dps_waitdone(self, sock:socket.socket, cookie):
        while True:
            results: str = DATABASE.hget("waitdone_despose_results", cookie)
            if results:
                sock.sendall(results.encode())
                sock.close()
                break

                
