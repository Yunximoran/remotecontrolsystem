import os
import subprocess
import platform
import socket
import uuid
import re
import inspect
import pickle
from xml.etree import ElementTree as et


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
    
    def __dump_system_model(self, SYSTEM, name, version, archiecture, softwarepath):
        with open("system.py", "w", encoding="utf-8") as f:
            f.write("import os\n")
            f.write("import re\n")
            f.write("import subprocess\n")
            f.write(inspect.getsource(BaseSystem))
            f.write("\n")
            f.write(inspect.getsource(SYSTEM))
            f.write(f'SYSTEM = {SYSTEM.__name__}("{version}", {archiecture}, "{softwarepath}")\n')
        
        
class BaseSystem:
    SOFTWARE_PATH = "" # 默认软件安装位置
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
    
    # 处理器
    def __get_tasklist(self):
        pass
    
    def __find_software(self, software):
        for root, dirs, files in os.walk(self.SOFTWARE_PATH):
            for fn in files:
                if fn == software:
                    return os.path.join(root, fn)
                else:
                    continue
                
                

class WindowsSystem(BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        
    def close(self):
        os.system("shutdown /s /t 1")
    
    def restart(self):
        os.system("shutdown /r/ t/ 1")
    
    def start_software(self, software):
        # 软件路径
        if software is not None:
            # 这里存在特殊情况，执行启动软件时，如果软件正在运行，删除软件可能不会有效果
            self.PID[software] = subprocess.Popen(software, stderr=subprocess.PIPE)
        else:
            raise FileExistsError(f"software {software} not installed")
    
    def close_software(self, software):
        # 这里存在问题，如果软件不是通过客户端运行的话
        process = subprocess.Popen("tasklist", stdout=subprocess.PIPE)
        stdout, _ = process.communicate()
        tasklist = [re.split("\s{2,}", task) for task in stdout.split("\n")[3: ]]
    
    def __get_tasklist(self):
        results = subprocess.Popen(['tasklist'], stdout=subprocess.PIPE, text=True)
        output, _ = results.communicate()
        tasklist =  [re.split(r"\s{2,}")  for task in output.split("\n")[3:]]
        

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
    import time
    Init()
