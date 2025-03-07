import subprocess
import re
import os

from ._base import __BaseSystem
from lib import Resolver
from pathlib import Path
resolver = Resolver()
ROOTPASS = resolver("computer")["password"]

class Linux(__BaseSystem):
        
    # 用户权限
    def close(self):
        return self.executor(["sudo", "shutdown", "now"], isadmin=True)
    
    def restart(self):
        os.system("sudo shutdown -r")
        return self.executor(["sudo", "shutdown", "-r"], isadmin=True)
        
    def start_software(self, software):
        return self.executor(["start", software])
    
    def close_software(self, software):
        self.PID[software].kill()
    
    def compress(self, ftype, f, t):
        """
            压缩
        """
        # 区分不同的tar指令 格式化默认参数
        if ftype == "tar":
            attr = "-cvf"
        if ftype == "bz2":
            attr = "-jcvf"
        if ftype == "gz":
            attr = "-zcvf"
        self.executor(["tar", attr, f, t])
    
    def uncompress(self, pack, to):
        """
            解压缩
        pack 文件地址
        to: 保存位置
        """
        ftype = Path(pack).suffix
        # ftype = pack.split(".")[-1]
        if ftype == ".tar":
            attr = "-xvf"
        if ftype == ".bz2":
            attr = "-jxvf"
        if ftype == ".gz":
            attr = "-zxvf"
        # 统一使用tar指令执行解压缩
        return self.executor(['tar', attr, pack, "-C", to])
    
    def wget(self, url, path=None):
        # 网络请求
        return super().wget(url, path)
    
    def remove(self, oldPath, newPath=None):
        return super().remove(oldPath, newPath)
    
    def executor(self, args, label=None, isadmin=False):
        """
            args: 指令参数
            label: 软件名
            isdamin: 是否需要管理员权限
        """
        process= subprocess.Popen(
                args=args,
                shell=True, 
                text=True,
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        if isadmin:
            # 如果需要管理员权限，通过communicate输入密码
            msg, err = process.communicate(ROOTPASS)
        else:
            msg, err = process.communicate()
        
        # 如果label不为空，则运行软件
        if label is not None:
            # 软件名称
            self.PID[label] = process
            
        return  self.report(args, msg, err)\
        if re.match("权限", err)\
        else self.executor(args, label, True)
    