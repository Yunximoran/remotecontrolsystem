import subprocess
import re
import os

from ._base import __BaseSystem
from lib import Resolver

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
        if ftype == "tar":
            attr = "-cvf"
        if ftype == "bz2":
            attr = "-jcvf"
        if ftype == "gz":
            attr = "-zcvf"
        self.executor(["tar", attr, f, t])
    
    def uncompress(self, pack, to):
        ftype = pack.split(".")[-1]
        if ftype == "tar":
            attr = "-xvf"
        if ftype == "bz2":
            attr = "-jxvf"
        if ftype == "gz":
            attr = "-zxvf"
        return self.executor(['tar', attr, pack, "-C", to])
    
    def wget(self, url, path=None):
        return super().wget(url, path)
    
    def remove(self, oldPath, newPath=None):
        return super().remove(oldPath, newPath)
    
    def executor(self, args, label=None, isadmin=False):
        process= subprocess.Popen(
                args=args,
                shell=True, 
                text=True,
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        if isadmin:
            msg, err = process.communicate(ROOTPASS)
        else:
            msg, err = process.communicate()
        
        if label is not None:
            # 软件名称
            self.PID[label] = process
            
        return  self.report(args, msg, err)\
        if re.match("权限", err)\
        else self.executor(args, label, True)
    