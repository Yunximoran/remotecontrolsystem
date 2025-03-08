import json
import time
from typing import Dict, Tuple, AnyStr

from ._prototype import TCP, socket
from gloabl import DB
from lib import CatchSock
from lib.sys.processing import MultiProcess
from lib import Resolver

resolver = Resolver()
catch = CatchSock()

ENCODING = resolver("project", "encoding")
RECVSIZE = resolver("sock", "recv-size")
DELAY = resolver("preformance", "while-delaytime")

class Listener(TCP):
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        
    @catch.timeout
    def recv(self, isblock=False) -> Dict[AnyStr, Tuple[socket.socket, AnyStr]]:
        sock, addr = self.sock.accept()
        # 是否需要阻塞，客户端连接
        sock.setblocking(1) if isblock else None 

        # 格式化TCP数据
        data = sock.recv(RECVSIZE)
        return sock, addr, sock

    def listen(self):
        """
            TCP监听器
        监听来自客户端的TCP连接
        主要接受reports, 
        """
        while True:
            # 接受客户端连接
            conn = self.recv(isblock=False)
            if conn is False:
                continue
            else:
                task = MultiProcess(target=self.__task, args=(conn, ))
                task.start()

             
    def __task(self, conn: Dict[AnyStr, Tuple[socket.socket, AnyStr]]):
        # 任务包装器
        """
            解析连接对象
        """
        sock, _, data = conn
        
        # 解析TCP数据，获取事件类型和cookie
        type, cookie = self._parse(data)
        
        # 事件分流
        self._event_brench(type, cookie, sock, data)
        
    def _parse(data):
        """
            解析TCP数据
        返回 事件类型 和 Cookie
        """
        msg = json.loads(data)
        event_type = msg['type']
        cookie = msg['cookie']
        return event_type, cookie

    def _event_brench(self, type, cookie, sock, data):
        """
            事件分支
        区分不同类型事件，执行对应事件
        """
        if type == "instruct":
            pass
                
        if type == "software":
            # 添加待办事件， 将事件标识和事件信息写入redis， 发送客户端，等待客户端处理
            self._add_waitdone(cookie, data)
            
            # 等待处理待办事件，定期搜索事件标识，如果找到，获取处理结果，返回客户端，关闭连接
            is_OK = self._dps_waitdone(cookie, sock)
            if not is_OK:
                # 在这里写入日志
                # 删除待办事项
                pass      
                
        if type == "report":
            # 将汇报结果保存数据库，执行日志
            DB.lpush("logs", data)

                      
    def _add_waitdone(self, cookie, data):
        DB.hset("waitdones", cookie, data)
        return cookie
    
    
    @catch.checksockconning
    def _dps_waitdone(self, sock:socket.socket, cookie):
        while True:
            if DB.hget("waitdones", cookie):
                # 校验待办事项是否被删除
                break

            results: str = DB.hget("waitdone_despose_results", cookie)
            if results:
                sock.sendall(results.encode())
                sock.close()
                return True
            
            time.sleep(DELAY)
        return False

