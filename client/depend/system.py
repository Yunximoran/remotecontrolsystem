import os
import re
import sys
import time
import json
import subprocess
from collections.abc import Iterable


from despose import CONFIG


import ctypes
import string
class BaseSystem:
    # 获取工作目录
    CWDIR = os.getcwd()
    # 运行文件
    DATAPATH = {
        # 路径依赖
        "softwares": os.path.join(CWDIR, r"local\data\softwares.json"),
        "root": None,
        "logs":{
            "msg": "local\logs\msg.log",
            "err": "local\logs\err.log",
        }
    }
    
    
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
        # 查找文件
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
    
    def executor(self, args, label=None):
        """
        :param label: PID标识
        :param args: 封装的shell指令列表
        :return report: 返回报文, 用于向服务端汇报执行结果
        
        除了软件清单，其他指令可能存在创建重复label进程
            如：同时关闭多个软件
            规定更详细的label close ？ softwares
        """
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
            # 软件名称
            self.PID[label] = process
            
        return  msg, err
    
        
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
            建立软连接
        :param filename: 指定软件名称
        :param frompath: 本地软件地址
        """
        # 创建软件映射地址
        topath = os.path.join(os.getcwd(), CONFIG.LOCAL_DIR_SOFTWARES, filename)   
        report = self.executor(["mklink", topath, frompath], isadmin=True)
        return topath, report

    def executor(self, args, label=None, isadmin=False):
        if isadmin:
            self.uproot()
        msg, err =  super().executor(args, label)
        return self.report(args, msg, err)\
        if not re.match("权限", err)\
        else self.executor(args, label, True)
    
    def uproot(self):
        # 不确定包含范围
        if self.is_admin():
            pass
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
            
    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
SYSTEM = WindowsSystem("10.0.26100", ('64bit', 'WindowsPE'))
