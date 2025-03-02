import json
import time
import socket
from typing import Dict, AnyStr

from ._prototype import UDP
from lib.sys.processing import Process, Value, Lock
from databasetool import Redis


RECVSIZE = 1024
MAXTASKS = 10
NOWTASKS = Value("i", 0)

lock = Lock()

def _readvalue():
    lock.acquire()
    value = NOWTASKS.value
    lock.release()
    return value

def _addvalue():
    lock.acquire()
    NOWTASKS.value += 1
    lock.release()
    
def _downvalue():
    lock.acquire()
    NOWTASKS.value -= 1
    lock.release()

class BroadCastor(UDP):
    """
    listen:
        启动监听
    
    task:
        注册每次接收到广播的任务
    """
    timers: Dict[AnyStr, Process]= {}
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    
    def listen(self):
        """
            注册监听任务
        """
        while True:
            nowtasks = _readvalue()
            if nowtasks < MAXTASKS:
                Process(target=self._task, args=()).start()
                _addvalue()
    
    def _uptasks(self, isadd=True):
        lock.acquire()
        NOWTASKS.value += 1
        lock.release()
    
    def _downtask(self):
        lock.acquire()
        NOWTASKS.value -= 1
        lock.release()
    
    def _task(self):
        # 接受广播数据
        # recvfrom 会阻塞进程，直到接收到数据
        res = self.sock.recvfrom(RECVSIZE)
        _downvalue()
        
        # 解析广播数据
        data = res[0].decode("utf-8")
        ip = json.loads(data)['ip']
        
        # 保存/更新 广播数据
        Redis.hset("client_status", ip, "true")
        Redis.hset("heart_packages", mapping={ip: data}) # ip地址和心跳包数据
        
        # 启动/更新 计时器
        try:
            timer = self.timers[ip]
            if timer.is_alive():
                # 如果计时进程仍在运行，立即停止
                timer.terminate()
            
            # 创建新的计时进程
            self.timers[ip] = Process(target=self.__timer, args=(ip, ))
        except KeyError:
            # 与ip对应的计时器不在字典中，创建他
        
            self.timers[ip] = Process(target=self.__timer, args=(ip, ))

        
    def __timer(self, ip):
        # 计时器
        """
            超过3秒没有更新心跳包关闭连接
            删除计时器
        """
        time.sleep(3)
        Redis.hset("client_status", ip, "false")
        Redis.hdel("heart_packages", ip)
        del self.timers[ip]
        print(f"The IP {ip} user is disconnected")     
        
            