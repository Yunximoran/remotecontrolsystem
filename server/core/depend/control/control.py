import socket
import struct
import json
from functools import partial

from lib.sys.processing import(
    Pool,
    Process,
    Lock,
    Queue
)
from databasetool import Redis
from core.depend.protocol.tcp import Connector



LOCK = Lock()
MESSAGEQUEUE = Queue()
WAITDONEQUEUE = Queue()


class Control:
    """
        控制模块
    负责与客户端之间的通信
    """
    process:list[Process] = []
    waittasks: dict[str, socket.socket] = {}
    
    def __init__(self):
        pass

    @staticmethod
    def stderr(err):
        print(err)
        
    @staticmethod
    def stdout(res):
        print(res)
    
    def sendtoclient(self, toclients, instructs=None, files=None):
        """
            多进程启动数据链接 依次发送指令
            加载redis中保存的client message
            子进程启动tcp连接客户端发送shell_control
        """
        # 未指定ip时，默认发送至所有正在链接的客户端
        # 检查链接客户端链接状体
        
        # 校验客户端连接
        toclients = self.checkconnect(toclients)
        
        # 向正在连接的指定客户端发送数据包
        with Pool() as pool:
            # 区分数据包类型
            if instructs is not None:
                # 发送指令数据
                print("send instruct")
                sendto = partial(self.sendtoshell, instructs=instructs)
            
                pool.map_async(sendto, toclients, 
                               callback=self.stdout,
                               error_callback=self.stderr)
                
            if files is not None and len(files) > 1:
                # 发送文件数据
                print("send files")
                sendto = partial(self.sendtofile, files=files)
            
                pool.map_async(sendto, toclients,
                            callback=self.stdout,
                            error_callback=self.stderr)
            
        
    @staticmethod                           
    def sendtofile(ip, file):
        # 发送文件数据
        conn = Connector()
        conn.sendfile(ip, file)
    
    @staticmethod
    def sendtoshell(ip, instructs):
        # 发送指令包
        print(ip, instructs)
        for instruct in instructs:
            conn = Connector()
            report =conn.send(ip, instruct)
            print("add report", report, type(report))
            Redis.hset("reports", ip, report)

        
    def checkconnect(self, toclients, status="true"):
        # 校验client连接状态
        connings = []
        clients = toclients if toclients != [] else Redis.hgetall("client_status")
        print("clients", clients)
        for ip in clients:
            if clients[ip] == status:
                connings.append(ip)
        return connings
    
    def sendwol_allclient(self, toclients=[]):
        # 校验客户端连接状态
        toclients = self.checkconnect(toclients=toclients, status="false")
        
        # 向所有客户端发送数据
        for ip in toclients:
            self.sendwol(ip)
            
    def sendwol(self, ip):
        # 创建UDP广播套接字
        broadcast = ("", 8085)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # 创建唤醒魔术包
        magic_pack = self.create_magic_packet(ip)
        # 发送广播
        sock.sendto(magic_pack, broadcast)
        
    
    def formatMAC(self, ip) -> str:
        """
            格式化mac码
        """
        # 读取对应ip客户端心跳包数据，获取MAC地址
        hreart_package = json.loads(Redis.hget("hreart_packages", ip))
        MAC:str = hreart_package["MAC"]
        
        # 校验MAC格式
        if len(MAC) == 12:
            return MAC
        if len(MAC) == 17:
            if MAC.count(":") == 5 or MAC.count("-") == 5:
                sep = MAC[2]
                MAC = MAC.replace(sep, '')
                return MAC
            else:
                raise ValueError("incorrect MAC format")
        else:
            raise ValueError("incorrect MAC format")
    
    def create_magic_packet(self, ip) -> bytes:
        """
            创建唤醒魔术包
        """
        mac = self.formatMAC(ip)
        data = b'FF' * 6 + (mac * 16).encode()
        print(data, type(data))
        send_data = b''
        
        for i in range(0, len(data), 2):
            send_data =send_data + struct.pack(b"B", int(data[i: i+2], 16))
        return send_data
    

class WOL:
    def __init__(self):
        pass