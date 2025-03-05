import os
import json
import sys
import ctypes
import string
import platform
import re

from ._base import __BaseSystem
from depend.path import *

SYSTEM_NAME = platform.system()                 # 操作系统名称
SYSTEM_VERSION = platform.version()             # 操作系统版本
SYSTEM_ARCHITECTURE = platform.architecture()   # 操作系统位数


PATH_SOFTWARES = None # input("")               # 软件安装路径
ROOTPASS = None # input("配置管理员密码")        # linux中需要设置管理员密码



def __uproot():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
        
class Windows(__BaseSystem):
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
        # 关机
        os.system("shutdown /s /t 3")
        return self.report(['shutdown', "/s", "/t", 1], "closed", False)
    
    def restart(self):
        # 重启
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
                        tosoftware = os.path.join(PATH_MAP_SOFTWARES, software)
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
    
    def build_hyperlink(self, filename, frompath, topath):
        """
            建立软连接
        :param filename: 指定软件名称
        :param frompath: 本地软件地址
        """
        # 创建软件映射地址
        # topath = os.path.join(os.getcwd(), CONFIG.LOCAL_DIR_SOFTWARES, filename)
        report = self.executor(["mklink", topath, frompath], isadmin=True)
        return topath, report

    def executor(self, args, label=None, isadmin=False):
        """
            shell执行器
        args: 执行的shell指令
        """
        # 是否需要管理员运行
        # if isadmin:
        #     # 如果需要检查当前权限状态，如无管理员权限则进行提权
        #     __uproot()
         # 是否需要管理员运行,需要检查当前权限状态，如无管理员权限则进行提权
        __uproot() if isadmin else None
        # 执行shell， 获取其输出信息和异常信息
        msg, err =  super().executor(args, label)
        
        # 返回执行结果， 检查是否由于权限导致的错误，如果是，改用管理员运行
        return self.report(args, msg, err)\
        if not re.match("权限", err)\
        else self.executor(args, label, True)
    