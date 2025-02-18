import socket
import struct
import json
from functools import partial

from projectdesposetool.systool.processing import(
    Pool,
    Process,
    Lock,
    Queue
)
from databasetool import DataBaseManager as DATABASE
from core.depend.protocol.tcp import TCPConnect



LOCK = Lock()
MESSAGEQUEUE = Queue()
WAITDONEQUEUE = Queue()


class Control:
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
        toclients = self.checkconnect(toclients)
        with Pool() as pool:
            if instructs is not None:
                print("send instruct")
                sendto = partial(self.sendtoshell, instructs=instructs)

            if files is not None and len(files) > 1:
                print("send files")
                sendto = partial(self.sendtofile, files=files)
            
            results = pool.map_async(sendto, toclients,
                           callback=self.stdout,
                           error_callback=self.stderr)
            
            results.wait()
        
    @staticmethod                           
    def sendtofile(ip, file):
        conn = TCPConnect()
        conn.sendfile(ip, file)
    
    @staticmethod
    def sendtoshell(ip, instructs):
        print(ip, instructs)
        for instruct in instructs:
            conn = TCPConnect()
            report =conn.send(ip, instruct)
            print("add report", report, type(report))
            DATABASE.hset("reports", ip, report)

        
    def checkconnect(self, toclients, status="true"):
        # 校验client连接状态
        connings = []
        clients = toclients if toclients != [] else DATABASE.hgetall("client_status")
        print("clients", clients)
        for ip in clients:
            if clients[ip] == status:
                connings.append(ip)
        return connings
    
    def sendwol_allclient(self, toclients=[]):
        toclients = self.checkconnect(toclients=toclients, status="false")
        for ip in toclients:
            self.sendwol(ip)
            
    def sendwol(self, ip):
        broadcast = ("", 8085)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        magic_pack = self.create_magic_packet(ip)
        sock.sendto(magic_pack, broadcast)
        
    
    def formatMAC(self, ip):
        hreart_package = json.loads(DATABASE.hget("hreart_packages", ip))
        MAC:str = hreart_package["MAC"]
        if len(MAC) == 12:
            pass
        if len(MAC) == 17:
            if MAC.count(":") == 5 or MAC.count("-") == 5:
                sep = MAC[2]
                MAC = MAC.replace(sep, '')
            else:
                raise ValueError("incorrect MAC format")
        else:
            raise ValueError("incorrect MAC format")
        return MAC
    
    def create_magic_packet(self, ip):
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