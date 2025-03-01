import json

from ._prototype import TCP, socket
from databasetool import Redis
from dispose import CONFIG
from dispose import CatchSock
from dispose.sys.processing import Process

Catch = CatchSock()
class Listener(TCP):
    """
    
    """
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        # self.sock.setblocking(1)  # 显式设置为阻塞模式
        
    @Catch.timeout
    def recv(self):
        sock, addr = self.sock.accept()
        sock.setblocking(1)  # 设置客户端socket为阻塞模式
        # 使用新接受的客户端socket进行接收操作
        data = sock.recv(1024)
        return sock, addr, data.decode()

    def listen(self):
        """
            监听器
        """
        while True:
            # 接受客户端连接
            conn = self.recv()
            if conn:
                # 创建处理任务
                task = Process(target=self.__task, args=(conn, ))
                task.start()
            else:
                pass
             
    def __task(self, conn):
        # 任务包装器
        """
            解析连接对象
        """
        sock, addr, data = conn
        # 格式化连接数据
        event_type, cookie = self._parse(data)
        # 对不同累心事件进行分流
        self._event_brench(event_type, cookie, data, sock)
        
    def _parse(data):
        """
            解析TCP数据
        返回 事件类型 和 Cookie
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
            self._add_waitdone(cookie, data)
            self._dps_waitdone(cookie, sock)          
                
        if t == "report":
            """
                获取汇报结果
            客户端控制指令执行结果返回服务端
            服务端保存至redis数据库
            yumo
            """
            Redis.lpush("logs", data)

                      
    def _add_waitdone(self, cookie, msg):
        Redis.hset("waitdones", cookie, msg)
        """
        前端通过接口返回处理结果，怎么找到对应的client套接字
        """
        return cookie
    
    @Catch.sock
    def _dps_waitdone(self, sock:socket.socket, cookie):
        while True:
            results: str = Redis.hget("waitdone_despose_results", cookie)
            if results:
                sock.sendall(results.encode())
                sock.close()
                break


if __name__ == "__main__":
    pass
