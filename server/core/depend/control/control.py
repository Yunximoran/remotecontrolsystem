import socket
import struct
import re, time
import json
from pathlib import Path
from functools import partial
from fastapi import UploadFile
from lib.sys.processing import(
    Pool,
    Process,
)
from lib import Resolver
from lib.manager._logger import Logger
from static import DB
from lib.sys.network import NetWork as NET
from core.depend.protocol.tcp import Connector
from datamodel.instruct import Instruct


resolver = Resolver()
logger = Logger("control", log_file="control.log")



# 广播地址
SERVERIP = resolver("network", "ip")
FILEPORT = resolver("ports", "tcp", "client-file")

LOCALPATH = resolver("path", "local")

class Control:
    """
        控制模块
    负责与客户端之间的通信
    
    
    sendtoclient
    
    sendtoshell
    sendtofile
    sendtowol
    """
    process:list[Process] = []
    waittasks: dict[str, socket.socket] = {}
    
    def __init__(self):
        pass
    
    def sendtoclient(self, toclients, *, instructs=None, files:list[Path] = None, wol=False):
        """
            多进程启动数据链接 依次发送指令
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
        # 未指定ip时，默认发送至所有正在链接的客户端
        # 检查链接客户端链接状体
        
        # 校验客户端连接, 对目标地址群进行状态分类
        toclients = self.__checkclientstatus(toclients)
        # 向正在连接的指定客户端发送数据包
        Process(target=self._send_tasks, args=(toclients, ), kwargs={
            "instructs": instructs,
            "files": files,
            "wol": wol
        }).start()
        
    
    def _send_tasks(self, toclients, instructs=None, files=None, wol=False):
        connings, breaks = toclients
        with Pool() as pool:
            if instructs is not None:
                # 发送指令数据
                logger.record(1, f"{instructs}")
                sendto = partial(self.sendtoshell, instructs=instructs)
                pool.map_async(sendto, connings, 
                               attribute={  # 使用偏函数后对丢失某些属性，通过attribute参数手动设置
                                   "__name__": self.sendtoclient.__name__
                                   }
                               ).get()
                
            if files is not None:
                # 发送文件数据
                sendto = partial(self.sendtofile, files=files)
                pool.map_async(sendto, connings, 
                               attribute={  # 使用偏函数后对丢失某些属性，通过attribute参数手动设置
                                   "__name__": self.sendtofile.__name__
                                   }
                               ).get()
                
            if wol:
                # 发送唤醒魔术包
                pool.map_async(self.sendtowol, breaks).get()
 
    @staticmethod                           
    def sendtofile(ip, files:list[Path]): # 发送文件数据
        # 创建下载指令
        heart_packages = DB.loads(DB.hget("heart_packages", ip))
        instruct = Instruct(label="download", instruct="file", os=heart_packages['os']).model_dump_json()
        
        # 发送指令，通知客户端准备接收文件
        conn = Connector()
        conn.connect(ip)
        conn.send(json.dumps([instruct], ensure_ascii=False, indent=4))
        is_OK = conn.recv()   # 客户端准备就绪
        
        if is_OK == "OK":
            logger.record(1, f"The client: {ip} is ready")
            # 建立文件传输通道
            file_conn = Connector()
            file_conn.sock.connect((ip, FILEPORT))
            file_conn.send(str(len(files))) # 发送的文件数量
            for file in files:
                if not file.exists():
                    # 如果路径不存在就从local目录中查找文件
                    local = LOCALPATH.bind(Path.cwd())
                    items = [item for item in local.rglob(file.name) if item.is_file()]
                    sendata = items[0]
                else:
                    sendata = file
                print(sendata)
                with open(sendata, "rb") as f:
                    filename = sendata.name    # 文件名称
                    filesize = str(sendata.stat().st_size) # 文件大小
                    logger.record(1, f"send file: {filename} start")    # 开始发送
                    file_conn.send(filename)    # 发送文件名
                    file_conn.send(filesize)    # 发送文件大小
                    file_conn.sock.sendfile(f)  # 发送文件数据
                    status = file_conn.recv()
                    logger.record(1, status)
            logger.record(1, "All the files have been received")
        else:
            logger.record(3, f"Client: {ip} preparation exception")
        
        file_conn.close()
        conn.close()
        
    @staticmethod
    def sendtoshell(ip, instructs):
        # 发送指令包
        conn = Connector()
        conn.connect(ip)
        logger.record(1, f"send: {instructs} to {ip}")
        conn.send(json.dumps(instructs, ensure_ascii=False, indent=4))
        reports = conn.recv()
        DB.hset("reports", ip, reports)
        conn.close()

    @staticmethod
    def sendtowol(ip):
        # 创建UDP广播套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # 创建唤醒魔术包
        hreart_package = json.loads(DB.hget("heart_packages", ip))
        MAC:str = hreart_package["mac"]
        magic_pack = NET.create_magic_packet(MAC)
        
        # 发送广播
        logger.record(1, f"send wol protocol to {ip}")
        sock.sendto(magic_pack, ("", 9))    

    def __checkclientstatus(self, toclients):
        """
            # 校验client连接状态
            
        toclients: 目标地址群
        status: 目标状态
        """
        connings = []
        breaks = []
        
        # 如果toclients是空列表，默认获取所有客户端
        if toclients == []:
            clients = DB.hgetall("client_status")
            
            # 遍历地址群 返回 连接指定状态的客户端
            for ip in clients:
                if clients[ip] == "true":
                    connings.append(ip)
                else:
                    breaks.append(ip)
        else:
            for ip in toclients:
                if DB.hget("client_status", ip) == "true":
                    connings.append(ip)
                else:
                    breaks.append(ip)
                    
        return connings, breaks
    

            

    
 
    
    