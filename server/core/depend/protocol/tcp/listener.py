import json
import time
from typing import Dict, Tuple, AnyStr

from core.depend.protocol.tcp._prototype import TCP, socket
from static import DB
from lib import CatchSock
from lib.sys.processing import Process, Value
from lib import Resolver

resolver = Resolver()
catch = CatchSock()

# ADDRESS = resolver("network", "ip")
# PORT = resolver("ports", "tcp", "server")
ENCODING = resolver("global", "encoding")
RECVSIZE = resolver("sock", "recv-size")
TIMEOUT = resolver("sock", "tcp", "timeout")
LISTENES = resolver("sock", "tcp", "listenes")
DELAY = 1

class Listener(TCP):
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(TIMEOUT)
        self.sock.listen(LISTENES)
    
    @catch.timeout
    def accept(self):
        sock, addr = self.sock.accept()
        return sock, addr

    @catch.sock
    def recv(self) -> Dict[AnyStr, Tuple[socket.socket, AnyStr]]:
        conn = self.accept()
        if conn:
            sock, addr = conn
            data = sock.recv(RECVSIZE)
            return sock, addr, data.decode(ENCODING)
        return False
    
    def listen(self):
        """
            TCP监听器
        监听来自客户端的TCP连接
        主要接受reports, 
        """
        while True:
            # 接受客户端连接
            try:
                conn = self.recv()
                if conn:
                    task = Process(target=self._task, args=(conn, ))
                    task.start()
            except KeyboardInterrupt:
                exit()
     
    def _task(self, conn: Dict[AnyStr, Tuple[socket.socket, AnyStr]]):
        # 任务包装器
        """
            解析连接对象
        """
        sock, addr, data = conn
        
        # 解析TCP数据，获取事件类型和cookie
        type, cookie = self._parse(data)
        
        # 事件分流
        self._event_brench(sock, addr, type, cookie, data)
        
    def _parse(self, data):
        """
            解析TCP数据
        返回 事件类型 和 Cookie
        """
        msg = json.loads(data)
        event_type = msg['type']
        cookie = msg['cookie']
        return event_type, cookie

    def _event_brench(self, sock, addr, type, cookie, data):
        """
            事件分支
        区分不同类型事件，执行对应事件
        """
        if type == "instruct":
            # 这里将来执行交互式shell时可能会用到
            pass
        
        if type == "software":
             # 添加待办事件， 将事件标识和事件信息写入redis， 发送客户端，等待客户端处理
            self._add_waitdone(cookie, data)
            
            # 等待处理待办事件，定期搜索事件标识，如果找到，获取处理结果，返回客户端，关闭连接
            Process(target=self._dps_waitdone, args=(cookie, sock)).start()
   
        if type == "report":
            # 将汇报结果保存数据库，执行日志
            DB.lpush("logs", data)

                      
    def _add_waitdone(self, cookie, data):
        DB.hset("waitdones", cookie, data)
        return cookie
    
    
    def _dps_waitdone(self, cookie:str, sock:socket.socket) -> bool:
        while True:
            if DB.hget("waitdones", cookie) or self._check_status():
                # 校验待办事项是否被删除
                break
            
            results: str = DB.hget("waitdone_dispose_results", cookie)
            if results:
                # 如果为空
                sock.sendall(results.encode())
                sock.close()
                return True
            
            time.sleep(DELAY)
        return False
    
    @catch.status
    def _check_status(self, sock:socket.socket=None):
        try:
            sock.getpeername()
            return True
        except:
            return False
