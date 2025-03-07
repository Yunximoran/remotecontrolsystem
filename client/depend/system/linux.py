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
        self._disks = ["/"]
        
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
    
    def remove(self, path, *, isdir=False):
        return self.executor(\
            ["rm", path] if not isdir else ["rm", "-D", path]
            )
    
    def move(self, topath, frompath):
        return self.executor(["mv", topath, frompath])
    
    def build_hyperlink(self, alias, frompath):
        topath = Path(LOCAL_DIR_SOFT).joinpath(alias)
        report = self.executor(["ln", "-s", frompath, topath])
        return topath, frompath, report
        
    def uproot(self):
        if os.geteuid() != 0:
            subprocess.check_call(["sudo", sys.executable] + sys.argv)
            sys.exit(0)

    def executor(self, args, isadmin=False, *, cwd=None) -> str:
        """
            args: 指令参数
            label: 软件名
            isdamin: 是否需要管理员权限
        """
        # 格式化为shell字符串
        if isinstance(args, list):
            args = " ".join(map(str, args))

        # 处理需要管理元运行的命令
        password = None
        if isadmin:
            if not re.match("^(sudo)(\s(-S))", args) \
                and re.match("^(sudo)", args):
                # -S， 读取标准输入密码
                args = args.replace("sudo", "sudo -S")
            else:
                if not re.match("^(sudo)(\s(-S))", args):
                    args = " ".join(map(str, ["sudo -S", args]))

            password = ROOTPASS
        

        process= subprocess.Popen(
                args=args,
                shell=True, 
                text=True,
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        try:
            msg, err = process.communicate(input=password, timeout=10)
        except TimeoutError:
            msg, err = False, "TimeoutError"
    

        return  self.report(args, msg, err)\
        if not re.match("权限", err)\
        else self.executor(args, True)
