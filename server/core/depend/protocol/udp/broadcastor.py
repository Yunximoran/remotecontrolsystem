import json
import time
import socket
from typing import Dict

from core.depend.protocol.udp._prototype import UDP
from lib.sys.processing import MultiProcess, Value, Lock
from lib import Resolver
from lib.sys import Logger
from gloabl import DB


logger = Logger("udp", "udp.log")
resolver = Resolver()

RECVSIZE = resolver("sock", "recv-size")
MAXTASKS = 10

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
        nowtasks = Value("i", 0, lock=True)
        
        logger.record(1, "UDP Listening")
        while True:
            if nowtasks.value < MAXTASKS:
                # 创建一个进程， task + 1
                task = MultiProcess(target=self._task, args=(nowtasks, ))
                task.start()

                # 原子操作：nowtasks.value += 1（自动锁保证安全）
                with nowtasks.get_lock():  # 显式获取锁确保复合操作安全
                    nowtasks.value += 1

    
    def _task(self, nowtasks):
        # 接受广播数据
        # recvfrom 会阻塞进程，直到接收到数据
        try:
            res = self.sock.recvfrom(RECVSIZE)

            
            # 解析广播数据
            data = res[0].decode("utf-8")
            ip = json.loads(data)['ip']
            logger.record(1, f"conning for client: {ip}")
            
            # 保存/更新 广播数据
            DB.set(ip, "true")
            DB.expire(ip, 1)
            
            DB.hset("client_status", ip, "true")
            DB.hset("heart_packages", mapping={ip: data}) # ip地址和心跳包数据
            MultiProcess(target=self._timer, args=(ip, )).start()
        finally:
            with nowtasks.get_lock():
                nowtasks.value -= 1
                
    def _timer(self, ip):
        time.sleep(3)
        if not DB.get(ip):
            logger.record(1, f"The client Disconnected:{ip}")
        
