import json
import time
import socket
from typing import Dict

from core.depend.protocol.udp._prototype import UDP
from lib.sys.processing import MultiProcess, Value, Lock, Array, Queue, Manager
from lib import Resolver
from lib.sys import Logger
from gloabl import DB


tasknum = Value("i", 0, lock=Lock())
logger = Logger("udp", "udp.log")
resolver = Resolver()
RECVSIZE = resolver("sock", "recv-size")
MAXTASKS = 10





def _timer(ip):
    size = 0
    while size < 3:
        time.sleep(1)
        size += 1
        DB.hget(ip, "size")
    time.sleep(3)
    DB.hset("client_status", ip, "false")
    DB.hdel("heart_packages", ip)
    logger.record(1, f"The IP {ip} user is disconnected")

class BroadCastor(UDP):
    """
    listen:
        启动监听
    
    task:
        注册每次接收到广播的任务
    """
    timers: Dict[str, MultiProcess] = {}  # 使用Manager共享字典
    def settings(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    
    def listen(self):
        """
            注册监听任务
        """
        logger.record(1, "UDP Listening")
        while True:
            if tasknum.value < MAXTASKS:
                task = MultiProcess(target=self._task, args=(tasknum,))
                task.start()
                tasknum.value += 1

    
    def _task(self, nowtasks):
        # 接受广播数据
        # recvfrom 会阻塞进程，直到接收到数据
        res = self.sock.recvfrom(RECVSIZE)
        nowtasks.value -= 1

        
        # 解析广播数据
        data = res[0].decode("utf-8")
        ip = json.loads(data)['ip']
        logger.record(1, f"conning for client: {ip}")
        
        # 保存/更新 广播数据
        DB.hset(ip, mapping={
            "status": "true",
            "heart_packages": data,
            "size": 3
        })
        DB.expire(ip, 3)
        
        DB.hset("client_status", ip, "true")
        DB.hset("heart_packages", mapping={ip: data}) # ip地址和心跳包数据

        
