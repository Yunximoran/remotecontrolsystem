import os
import time
import subprocess
import platform
import socket
import uuid
import re
import inspect
import pickle
import sys
import ctypes
import json
import string
from collections.abc import Iterable
from xml.etree import ElementTree as et


from despose import CONFIG


SYSTEM_NAME = platform.system()                 # 操作系统名称
SYSTEM_VERSION = platform.version()             # 操作系统版本
SYSTEM_ARCHITECTURE = platform.architecture()   # 操作系统位数
IP = socket.gethostbyname(socket.gethostname()) # IP地址
MAC = hex(uuid.getnode())                       # MAC地址

PATH_SOFTWARES = None # input("")               # 软件安装路径
ROOTPASS = None # input("配置管理员密码")        # linux中需要设置管理员密码

def check_software_path(self):
    return input("配置软件安装路径: ")
    
class Init:
    """
        初始化项目
    """
    DUMPSYSTEM = {
        "public": [
            "import os",
            "import re",
            "import sys",
            "import time",
            "import json",
            "import subprocess", 
            "from collections.abc import Iterable",
            "\n",
            "from despose import CONFIG",
            "\n"
        ],
        "Windows":[
            "import ctypes",
            "import string"
        ],
        "Linux": [],
        "MacOS": []
    }
    def __init__(self, username=None, password=None):
        self.__init_system()  # 初始化操作系统
        self.__init_local_address(username, password) # 初始化本地IP、MAC
        
    def __init_local_address(self, username, password):
        tree = et.parse("config.xml")
        root = tree.getroot()
        root.set("ip", IP)
        root.set("mac", MAC)
        if username:
            root.set("user", username)
        if password:
            root.set("pass", password)
        tree.write("config.xml")

    def __init_system(self):
        if SYSTEM_NAME == "Windows":
            self.__dump_system_model(WindowsSystem, SYSTEM_NAME, SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
            

        elif SYSTEM_NAME == "Linux":
            self.__dump_system_model(LinuxSystem, SYSTEM_NAME, SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
        
        # elif SYSTEM_NAME == "macOS":
        #     return MacOSSytem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
        
        # else:
        #     return BaseSystem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
    
    def __dump_system_model(self, SYSTEM, label, version, archiecture):
        with open(r"depend\system.py", "w", encoding="utf-8") as f:
            for public_package in self.DUMPSYSTEM['public']:
                f.write(f"{public_package}\n")
            
            for private_package in self.DUMPSYSTEM[label]:
                f.write(f"{private_package}\n")
                
            
            f.write(inspect.getsource(BaseSystem))
            f.write(inspect.getsource(SYSTEM))
            f.write(f'SYSTEM = {SYSTEM.__name__}("{version}", {archiecture})\n')
        
    
        
        
        
class BaseSystem:
    CWDIR = os.getcwd()
    DATAPATH = {
        "softwares": os.path.join(CWDIR, r"local\data\softwares.json"),
        "root": None,
        "logs":{
            "msg": "local\logs\msg.log",
            "err": "local\logs\err.log",
        }
    }
    
    """
    存在问题
        设备关机和重启
    """
    
    PID:dict[str, subprocess.Popen] = {}  # 保存运行进程
    
    
    def __init__(self, version, architecure):
        self.version = version
        self.bit, self.linktype = architecure
    
    def init(self):
        pass
    
    
    # 硬件相关
    def close(self):
        # 关机
        pass
    
    def restart(self):
        # 重启
        pass
    
    
    # 软件相关
    def start_software(self, software):
        # 启动软件
        pass
    
    def close_software(self, software):
        # 关闭软件
        pass
    
    def format_params(self, typecode, data):
        types = [
            "instruct",
            "software",
            "report"
        ]
        return json.dumps({
            "type": types[typecode],
            "data": data,    # 携带的data， 软件路径列表 | 错误报文
            "cookie": time.time()
        }, ensure_ascii=False)
    
    # def wait_response(self, param):
    #     conn = TCPConnect()
    #     conn.send(json.dumps(param))
    #     data = conn.recv()
    #     conn.close()
    #     return data.decode()
    
    # 文件相关
    def compress(self, dir_path):
        # 压缩
        pass
    
    def uncompress(self, form, to):
        # 解压
        pass
    
    def wget(self, url, path=None):
        # 下载
        pass
    
    def remove(self, oldPath, newPath=None):
        # 移动文件或删除
        if newPath:
            pass
        else:
            print("del file")
            
    def checkfile(self, check_object, base=None):
        results = []
        if base is None:
            base = self.DATAPATH['root']
        for root, dirs, files in os.walk(base):
            for file in files:
                if file == check_object:
                    results.append(os.path.join(root, file))
            for dir in dirs:
                if dir == check_object:
                    results.append(os.path.join(root, dir))
                    
        return results
    
    def executor(self, args, label=None, isadmin=False):
        """
        :param label: PID标识
        :param args: 封装的shell指令列表
        :return report: 返回报文, 用于向服务端汇报执行结果
        
        除了软件清单，其他指令可能存在创建重复label进程
            如：同时关闭多个软件
            规定更详细的label close ？ softwares
        """
        if isadmin:
            self.uproot()
        process= subprocess.Popen(
                args=args,
                shell=True, 
                text=True,
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        msg, err = process.communicate()
        
        if label is not None:
            self.PID[label] = process
            
        return  self.report(args, msg, err)\
            if err == "你没有足够的权限执行此操作" or "权限不足"\
            else self.executor(args, isadmin=True)
    
        
    def report(self, args, msg, err):
        # 格式化报文
        return json.dumps({
            "status": "ok" if not err else "error",
            "instruct": " ".join(args) if isinstance(args, Iterable) else args,
            "msg": msg if msg else "<No output>",
            "err": err if err else "<No error output>",
            "time": time.time()
        }, ensure_ascii=False)   
    
    
    def build_hyperlink(self, frompath):
        pass
    
    def uproot(self):
        # 升级root权限
        pass
                

class WindowsSystem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        self.DATAPATH['root'] = self.__getdisks()
    
    def __getdisks(self):
        # window独有
        drives = []
        bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
        return drives
    
    def close(self):
        os.system("shutdown /s /t 3")
        return self.report(['shutdown', "/s", "/t", 1], "closed", False)
    
    def restart(self):
        os.system("shutdown /r /t 3")
        return self.report(["shutdown", "/r", "/t", 1], "restarted", False)
    
    def start_software(self, software):
        # 软件路径
        report = None
        with open(self.DATAPATH['softwares'], 'r', encoding="utf-8") as f:
            softwares = json.load(f)    # 软件映射文件
            for item in softwares:
                if software == item["ecdis"]['name']:
                    # 新窗口打开 防止进程已经开启 | 或者后续更新为校验进程池
                    try:
                        report = self.executor(["start", item['ecdis']['path']], label=software)
                    except:
                        tosoftware = os.path.join(CONFIG.PATH_MAP_SOFTWARES, software)
                        report = self.executor(["start", tosoftware], label=software)
                        
                    # 通过报文返回的信息，如果没有异常，表示正在连接
                    item["conning"] = True if report['err'] == "<No error output>" else False # 更新软件状态
                    break
                
        if report is None:
            # 如果 report为空，软件不存在，创建对应报文
            report = self.report(software, False, f"no found software: {software}")
        else:
            # 否则 更新本地数据
            with open(self.DATAPATH["softwares"], 'w', encoding="utf-8") as f:
                json.dump(softwares, f, ensure_ascii=False, indent=4)
        
        return report
        
            
    def close_software(self, software):
        # 这里存在问题，如果软件不是通过客户端运行的话
        # 解决：所有软件默认通过客户端运行，对应进程保存在PID中
        try:
            process = self.PID[software]
            process.kill()
        except:
            pass

    def checkfile(self, check_object):
        results = []
        for root in self.DATAPATH['root']:
            results.extend(super().checkfile(check_object, root))
        return results
    
    def build_hyperlink(self, filename, frompath):
        """
        target 目录名称
        所在路径
            linux 可以通过软链接启动程序
            window 软连接需要将包含软件依赖的目录
        """
        # windows 建立关联整个目录的连接
        topath = os.path.join(os.getcwd(), CONFIG.LOCAL_DIR_SOFTWARES, filename)  # 软件映射地址  
        # 软件不应该同名
        report = self.executor(["mklink", topath, frompath], isadmin=True)
        return topath, report

    def uproot(self):
        # 不确定包含范围
        if self.is_admin():
            pass
        else:
            
            # ShellExecuteW
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            # sys.exit(0)
            
    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
class LinuxSystem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        
    # 用户权限
    def close(self):
        subprocess.Popen("sudo shutdown nov")
        os.system("sudo shutdown now")
    
    def restart(self):
        os.system("sudo shutdown -r")
        
    def start_software(self, software):
        return super().start_software(software)
    
    def close_software(self, software):
        return super().close_software(software)

    def __update_admin(self):
        # 升级管理员权限
        # 密码在初始化时加载
        # 后续如果更新密码则同步更新
        process = subprocess.Popen(['su', '-p'], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        process.stdin.write(ROOTPASS)
    
        
class MacOSSystem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        
        
        
if __name__ == "__main__":
    """
    软件路径不一定要统一，但是可以配置安装路径
    """
    Init()
    