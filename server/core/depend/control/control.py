import socket
import struct
import json
from functools import partial

from lib.sys.processing import(
    MultiPool,
    MultiProcess,
)
from lib import Resolver
from lib.sys.logger import Logger
from gloabl import DB
from lib.sys.network import NetWork as NET
from core.depend.protocol.tcp import Connector


resolver = Resolver()
logger = Logger("control", log_file="control.log")



# 广播地址
BROADCAST = ("", resolver("udp", "broad"))

class Control:
    """
        控制模块
    负责与客户端之间的通信
    
    
    sendtoclient
    
    sendtoshell
    sendtofile
    sendtowol
    """
    process:list[MultiProcess] = []
    waittasks: dict[str, socket.socket] = {}
    
    def __init__(self):
        pass
    
    def sendtoclient(self, toclients, *, instructs=None, files=None, wol=False):
        """
            多进程启动数据链接 依次发送指令
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
        # 未指定ip时，默认发送至所有正在链接的客户端
        # 检查链接客户端链接状体
        
        # 校验客户端连接, 对目标地址群进行状态分类
        connings, breaks = self.__checkclientstatus(toclients)
        logger.record(1, f"{instructs}")
        # 向正在连接的指定客户端发送数据包
        with MultiPool() as pool:
            if instructs is not None:
                # 发送指令数据
                sendto = partial(self.sendtoshell, instructs=instructs)
                setattr(sendto, "__name__", self.sendtoshell.__name__)
                pool.map_async(sendto, connings).get()
                
            if files is not None and len(files) > 1:
                # 发送文件数据
                sendto = partial(self.sendtofile, files=files)
                pool.map_async(sendto, connings).wait()
                
            if wol:
                # 发送唤醒魔术包
                pool.map_async(self.sendtowol, breaks).wait()
            
             
                 
    @staticmethod                           
    def sendtofile(ip, file):
        # 发送文件数据
        logger.record(1, f"send file: {file}")
        conn = Connector()
        conn.sendfile(ip, file)
    
    @staticmethod
    def sendtoshell(ip, instructs):
        # 发送指令包
        conn = Connector()
        conn.connect(ip)
        logger.record(1, f"send: {instructs} to {ip}")
        conn.send(json.dumps(instructs, ensure_ascii=False, indent=4))
        report = conn.recv()
        if report['err'] == "error":
            logger.record(1, f"{ip} exec {instructs}: OK")
        else:
            logger.record(3, f"{ip} exec {instructs}: ERROR")
        DB.hset("reports", ip, report)
        print(conn)
        conn.close()
        # for instruct in instructs:
        #     # 创建TCP连接
            
        #     logger.record(1, f"send: {instruct} to {ip}")
        #     # 发送shell执行
        #     report =conn.send(instruct)
        #     # 记录执行日志，保存结果到redis
        #     if report["err"] != "error":
        #         logger.record(1, f"{ip} exec {instruct}: OK")
        #     else:
        #         logger.record(3, f"{ip} exec {instruct}: ERROR")
                
        #     # 不管结果如何都保存在redis
        #     DB.hset("reports", ip, report)

    @staticmethod
    def sendtowol(ip):
        # 创建UDP广播套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # 创建唤醒魔术包
        hreart_package = json.loads(DB.hget("hreart_packages", ip))
        MAC:str = hreart_package["MAC"]
        magic_pack = NET.create_magic_packet(MAC)
        
        # 发送广播
        logger.record(1, f"send wol protocol to {ip}")
        sock.sendto(magic_pack, BROADCAST)    

    def __checkclientstatus(self, toclients):
        """
            # 校验client连接状态
            
        toclients: 目标地址群
        status: 目标状态
        """
        connings = []
        breaks = []
        
        # 如果toclients是空列表，默认获取所有客户端
        clients = toclients if toclients != [] else DB.hgetall("client_status")
        
        # 遍历地址群 返回 连接指定状态的客户端
        for ip in clients:
            if clients[ip] == "true":
                connings.append(ip)
            else:
                breaks.append(ip)
        return connings, breaks
    

            

    
 
    
    