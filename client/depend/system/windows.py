import os
import json
import sys
import ctypes
import string
import re

from ._base import __BaseSystem
from depend.path import *



def _uproot():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
        
class Windows(__BaseSystem):
    def __init__(self, *args):
        super().__init__(*args)
        self._disks = self.__getdisks()
    
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
        # 读取本地软件清单
        with open(PATH_MAP_SOFTWARES, 'r', encoding="utf-8") as f:
            softwares = json.load(f)    # 软件映射文件
            for item in softwares:
                if software == item["ecdis"]['name']:
                    try:
                        report = self.executor(["start", item['ecdis']['path']], label=software)
                    except:
                        tosoftware = os.path.join(PATH_MAP_SOFTWARES, software)
                        report = self.executor(["start", tosoftware], label=software)
                        
                    # 更新软件状态
                    item["conning"] = True if report['err'] == "<No error output>" else False
                    break
                
        if report is None:
            # 如果 report为空，软件不存在，创建对应报文
            report = self.report(software, False, f"no found software: {software}")
        else:
            # 否则 更新本地数据
            with open(PATH_MAP_SOFTWARES, 'w', encoding="utf-8") as f:
                json.dump(softwares, f, ensure_ascii=False, indent=4)
        
        return report

            
    def close_software(self, software):
        """
            目标软件的唯一路径[实际地址]
        遍历进程池
        
        """
        parcpath = None
        with open(PATH_MAP_SOFTWARES, "r", encoding="utf-8") as f:
            softwares = json.load(f)
            
            # 查找应用所在位置
            for item in softwares:
                if item['ecdis']['name'] == software:
                    # 获取软件源地址
                    parcpath = item['ecdis']['parc-path']
                    break
        
        # 校验软件是否加入管理
        if parcpath is None:
            return self.report(software, False,  "软件未加入管理")
        
        # 执行关闭软件命令
        processes = self._check_soft_status(software, parcpath)
        for process in processes:
            process.kill()
        
        return self.report(software, f"{software} is killed", False)
    
    def search(self, obj, if_gloabl=False):
        pass
    
    def checkfile(self, check_object):
        results = []
        for root in self._disks:
            results.extend(super().checkfile(check_object, root))
        return results
    
    def build_hyperlink(self, alias, frompath):
        """
            建立软连接
        :param filename: 指定软件名称
        :param frompath: 本地软件地址
        """
        # 创建软件映射地址
        topath = os.path.join(LOCAL_DIR_SOFT, alias)
        # mlink 映射地址 实际地址
        report = self.executor(["mklink", topath, frompath], isadmin=True)
        return topath, frompath, report

    def executor(self, args, isadmin=False, *, cwd=None):
        """
            shell执行器
        args: 执行的shell指令
        """
        # 是否需要管理员运行
        # if isadmin:
        #     # 如果需要检查当前权限状态，如无管理员权限则进行提权
        #     __uproot()
         # 是否需要管理员运行,需要检查当前权限状态，如无管理员权限则进行提权
        _uproot()  if isadmin else None
        # 执行shell， 获取其输出信息和异常信息
        msg, err =  super().executor(args, cwd=cwd)
        # 返回执行结果， 检查是否由于权限导致的错误，如果是，改用管理员运行
        self.record(1, f"exec {args} results:\n{msg}")
        return self.report(args, msg, err)\
        if not re.match("权限", err)\
        else self.executor(args, isadmin=True, cwd=cwd)
