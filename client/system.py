import os
import re
import subprocess
class BaseSystem:
    SOFTWARE_PATH = "" # 默认软件安装位置
    # EXTENSION = ".exe" | ".deb"
    
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
        pass
    
    def restart(self):
        pass
    
    
    # 软件相关
    def start_software(self, software):
        pass
    
    def close_software(self, software):
        pass
    
    
    # 文件相关
    def compress(self, dir_path):
        """
            解压
        """
        pass
    
    def uncompress(self, form, to):
        """
            压缩
        """
        pass
    
    def wget(self, url, path=None):
        """
            下载
        """
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
SYSTEM = WindowsSystem("10.0.22631", ('64bit', 'WindowsPE'), "D://softwares/")
