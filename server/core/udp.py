import asyncio
import socket
import struct
import json

import databasetool
from projectdesposetool import CONFIG


SERVERADDRESS = (CONFIG.IP, CONFIG.USPORT)    # 服务端地址


BROADCAST = ("", CONFIG.UBPORT)                  # 配置UDP广播地址
MULTICAST = ("224.25.25.1", CONFIG.UMPORT)          # 配置UDP组播地址

# 
ENCODING = "utf-8"                           # 编码格式
RECVSIZE = 1024                              # 最大数据量
MAXCONNNUM = 50                              # 最大连接数
TIMEOUT = 3                                  # 超时等待时间
TIMERLIST = {}                               # 客户端连接状态
DATABASE = databasetool.RedisConn            # Redis数据库


class Communication:
    def __init__(self):
        self.udp_protocol = UPD()
        self.udp_protocol.run()
        
        
        
class UPD:
    """
        # 监听客户端连接状态
        # 向客户端发送软件清单
    """
    # RECEPTION_TASK_LIST = []
    
    def __init__(self):
        self.init_udp_socket() 
        self.loop = asyncio.get_event_loop()
        self.add_tasks()
        
    def add_tasks(self):
        # 创建模块任务
        self.loop.create_task(self.reception())
        
    def init_udp_socket(self):
        # 初始化UDP套接字
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # 声明UDP协议
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # 允许地址复用
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   # 允许地址复用
        self.udp_socket.bind(BROADCAST)     # 绑定本机地址

    async def reception(self):   # 加载数据连接模块
        self.recloop = asyncio.new_event_loop()
        self.loop.run_in_executor(None, Reception, self.recloop, self.udp_socket)
        

    def run(self):
        try:    # 事件循环
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()
            self.udp_socket.close()
    

    
class Reception:
    CONNECTNUM = 0  # 标记当前正在等待客户端连接的任务数量
    CLIENTSTART = {
        
    }
    
    def __init__(self, 
                 loop: asyncio.BaseEventLoop,
                 sock: socket.socket
                 ):
        
        self.loop = loop
        self.udp_socket = sock
        self.loop.create_task(self.reception())
        
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.close()
  
            
    async def reception(self):
        # 创建接收任务
        while True:
            while len(TIMERLIST) > MAXCONNNUM:
                continue
            self.loop.create_task(self.__reception())
            self.CONNECTNUM += 1
            await asyncio.sleep(0.1)    
     

    async def __reception(self):
        # 等待客户端发送数据(心跳包)
        rec = await self.loop.sock_recvfrom(self.udp_socket, RECVSIZE)
        self.CONNECTNUM -= 10
        
        # 解析数据
        data = rec[0].decode(ENCODING)
        ip = json.loads(data)['ip']
        # print(ip)
        # 保存心跳包数据
        DATABASE.hset("client_status", ip, "true")
        DATABASE.hset("heart_packages", mapping={ip: data}) # ip地址和心跳包数据
        
        # 校验客户端连接状态
        await self.__check_connection(ip)



    async def __check_connection(self, ip):
        if ip in TIMERLIST:
            # 校验当前客户端是否正在连接
            TIMERLIST[ip].cancel()
        
        # 创建计时器，并保存在CHECK_CONNSTART中
        timer = asyncio.create_task(self.__timer(ip))
        TIMERLIST[ip] = timer
        
        # 启动计时器
        try:
            await timer
        except asyncio.CancelledError:
            pass
            # print("重置计时器")
        

    async def __timer(self, ip):
        # 等待3秒后 删除客户端连接缓存 or 先标记为断线 等待服务端关闭后清空
        await asyncio.sleep(3)
        TIMERLIST.pop(ip)
        DATABASE.hset("client_status", ip, "false")   # 删除客户端连接数据
        DATABASE.hdel("heart_packages", ip)     # 删除心跳包
        print(f"The IP {ip} user is disconnected")


class MultiCast:
    def __init__(self):
        self.multi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.multi.bind(("", MULTICAST[1]))   # 绑定组播端口
    
    def settings(self):
        
        # 接受数据前加入组播组
        group = socket.inet_aton(MULTICAST[0])
        merq = struct.pack("4sL", group, socket.INADDR_ANY)
        self.multi.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, merq)
        
        
    
    def send(self, data:str):
        print(data)
        self.multi.sendto(data.encode(), MULTICAST)
        


if __name__ == "__main__":
    Communication()