import subprocess
import re
import os
import sys
from getpass import getpass
from ._base import __BaseSystem
from lib import Resolver
from depend.path import *


resolver = Resolver()
ROOTPASS = resolver("computer")["password"]

class Linux(__BaseSystem):
    def __init__(self):
        super().__init__()
        self._disks = [Path("/")]
        
    # 用户权限
    def close(self):
        return self.executor(["sudo", "shutdown", "now"], isadmin=True)
    
    def restart(self):
        os.system("sudo shutdown -r")
        return self.executor(["sudo", "shutdown", "-r"], isadmin=True)
        
    def start_software(self, path):
        path = self._path(path)
        report = self.executor([path.name], cwd=path.parent, iswait=False)
        return report
    
    def close_software(self, software):
        path = self._path(software)
        processes = self._check_soft_status(path)
        for process in processes:
            process.kill()

    
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
    
    def remove(self, path, *, isdir=False):
        return self.executor(\
            ["rm", path] if not isdir else ["rm", "-D", path]
            )
    
    def move(self, topath, frompath):
        return self.executor(["mv", topath, frompath])
    
    def build_hyperlink(self, topath:Path, frompath:Path):
        topath = self._path(topath)
        frompath = self._path(frompath)
        if not frompath.exists():
            raise "source file is not exists"
        
        if topath.exists():
            topath.unlink()
            
        topath = str(topath)# Path(LOCAL_DIR_SOFT).joinpath(alias)
        frompath = str(frompath)
        report = self.executor(["ln", "-s", frompath, topath])
        return topath, report
        
    def uproot(self, args:str) -> str:
        if not re.match(r"^(sudo)(\s(-S))", args) \
            and re.match(r"^(sudo)", args):
            # -S， 读取标准输入密码
            args = args.replace(r"sudo", "sudo -S")
        else:
            if not re.match(r"^(sudo)(\s(-S))", args):
                args = " ".join(map(str, ["sudo -S", args]))
        return args


    def executor(self, args, isadmin=False, *, cwd=None, iswait=True) -> str:
        """
            args: 指令参数
            label: 软件名
            isdamin: 是否需要管理员权限
        """
        # 格式化为shell字符串
        if isinstance(args, list):
            args = " ".join(map(str, args))

        if isadmin or re.match("^(sudo)", args):
            # 升级为管理员shell，并设置为从标准输入获取密码
            args = self.uproot(args)
            print(args)
            password = ROOTPASS
        else:
            password = None

        msg, err = super().executor(args, cwd=cwd,stdin=password, timeout=10, iswait=iswait)

        if err:
            self.record(3, f"exec {args} results:\n{err}")
        else:
            self.record(1, f"exec {args} results:\n{msg}")
        return  self.report(args, msg, err)\
        if not re.match("[(权限)|(password)|(密码)]", err)\
        else self.executor(args, True)
