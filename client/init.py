import os
import time
import subprocess
import platform
import socket
import uuid
import re
import inspect
import pickle
import ctypes
import json
import string
from collections.abc import Iterable
from xml.etree import ElementTree as et
from protocol import TCPConnect


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
            "import time",
            "import json",
            "import subprocess", 
            "from collections.abc import Iterable",
            "from protocol import TCPConnect"
        ],
        "Windows":[
            "import ctypes",
            "import string"
        ],
        "Linux": [],
        "MacOS": []
    }
    def __init__(self):
        self.__init_system()  # 初始化操作系统
        self.__init_local_address() # 初始化本地IP、MAC
        
    def __init_local_address(self):
        tree = et.parse("config.xml")
        root = tree.getroot()
        root.set("ip", IP)
        root.set("mac", MAC)
        tree.write("config.xml")

    def __init_system(self):
        if SYSTEM_NAME == "Windows":
            self.__dump_system_model(WindowsSystem, SYSTEM_NAME, SYSTEM_VERSION, SYSTEM_ARCHITECTURE, "D://softwares/")
            

        elif SYSTEM_NAME == "Linux":
            self.__dump_system_model(LinuxSystem, SYSTEM_NAME, SYSTEM_VERSION, SYSTEM_ARCHITECTURE, "~/softwares/")
        
        # elif SYSTEM_NAME == "macOS":
        #     return MacOSSytem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
        
        # else:
        #     return BaseSystem(SYSTEM_VERSION, SYSTEM_ARCHITECTURE)
    
    def __dump_system_model(self, SYSTEM, label, version, archiecture, softwarepath):
        with open(r"util\system.py", "w", encoding="utf-8") as f:
            for public_package in self.DUMPSYSTEM['public']:
                f.write(f"{public_package}\n")
            
            for private_package in self.DUMPSYSTEM[label]:
                f.write(f"{private_package}\n")
            f.write(inspect.getsource(BaseSystem))
            f.write(inspect.getsource(SYSTEM))
            f.write(f'SYSTEM = {SYSTEM.__name__}("{version}", {archiecture}, "{softwarepath}")\n')
        
    
        
        
        
class BaseSystem:
    CWDIR = os.getcwd()
    DATAPATH = {
        "softwares": os.path.join(CWDIR, r"data\softwares.json"),
        "root": None,
        "logs":{
            "msg": None,
            "err": None,
        }
    }
    ERRORFILE = {
        "file": None,
        "path": None
    }
    MSGFILE = {
        "file": None,
        "path": None
    }
    # EXTENSION = ".exe" | ".deb"
    
    """
    存在问题
        设备关机和重启
    """
    
    PID:dict[str, subprocess.Popen] = {}    # 暂定
    
    
    def __init__(self, version, architecure, softwares_dir=""):
        if not os.path.exists(softwares_dir):
            os.makedirs(softwares_dir)
        
        self.version = version
        self.bit, self.linktype = architecure
        self.path = {
            "softwares": softwares_dir
        }
    
    def init(self):
        pass
    
    def getdisks(self):
        drives = []
    
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
    
    def format_params(self, label, data):
        return {
            "label": label,
            "data": data
        }
    
    def wait_response(self, param):
        conn = TCPConnect()
        conn.send(json.dumps(param))
        data = conn.recv()
        conn.close()
        return data.decode()
    
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
            
    def checkfile(self, check_object, root=None):
        results = []
        if root is None:
            root = self.DATAPATH['root']
        for root, dirs, files in os.walk(root):
            for file in files:
                if file == check_object:
                    results.append(os.path(root, file))
            for dir in dirs:
                if dir == check_object:
                    results.append(os.path.join(root, dir))
                    
        return results
    
    def executor(self, label, args, isclear=True):
        """
        :param label: PID标识
        :param args: 封装的shell指令列表
        :return report: 返回报文, 用于向服务端汇报执行结果 
        """
        self.PID[label] = subprocess.Popen(args=args, shell=True, text=True,
                                           stdin = subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        msg, err = self.PID[label].communicate()
        self.clear_process(label) if isclear else None
        return self.report(args, msg, err) 
    
    def clear_process(self, label):
        # 清理无用进程
        self.PID[label].kill()
        del self.PID[label]
        
    def report(self, args, msg, err):
        # 格式化报文
        return {
            "status": "ok" if not err else "error",
            "instruct": " ".join(args) if isinstance(args, Iterable) else args,
            "msg": msg if msg else "<No output>",
            "err": err if err else "<No error output>",
            "time": time.time()
        }   
    
    def build_hyperlink(self, frompath):
        report = self.executor("build re")
    
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
        os.system("shutdown /s /t 1")
        return self.report(['shutdown', "/s", "/t", 1], "closed", False)
    
    def restart(self):
        os.system("shutdown /r/ t/ 1")
        return self.report(["shutdown", "/r", "/t", 1], "restarted", False)
    
    def start_software(self, software):
        # 软件路径
        report = None
        with open(self.DATAPATH['softwares'], 'r', encoding="utf-8") as f:
            softwares = json.load(f)
            for item in softwares:
                if software == item["ecdis"]['name']:
                    # 新窗口打开 防止进程已经开启 | 或者后续更新为校验进程池
                    report = self.executor(software, ["start", item['ecdis']['path']], False)
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
    
    def build_hyperlink(frompath):
        """
        target 目录名称
        所在路径
            linux 可以通过软链接启动程序
            window 软连接需要将包含软件依赖的目录
        """
        # windows 建立关联整个目录的连接
        target = os.path.basename(frompath)
        topath = os.path.join(".\local\softwares", target)
        subprocess.Popen(["mklink", "/j", topath, frompath])
        return topath
    
    def build_softwarelink(self, softname, frompath):
        path = r".\local\softwares\{name}".format(name=softname)
        self.executor(["mklink", "/j", path, frompath])
        return path
        
    
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
    
    def __execute_shell(self, shell):
        # 执行shell
        # 检测是否需要额外输入
        # 如果需要通知服务端处理
        process = subprocess.Popen(shell, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        
class MacOSSystem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        
        
        
if __name__ == "__main__":
    """
    软件路径不一定要统一，但是可以配置安装路径
    """
    Init()

    