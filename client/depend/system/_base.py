import os
import time
import subprocess
import platform
import socket
import uuid
import re
import inspect
import sys
import ctypes
import json
import string
from pathlib import Path
from collections.abc import Iterable
from xml.etree import ElementTree as et
from typing import Tuple
import psutil
from typing import Generator
from psutil import NoSuchProcess, AccessDenied
from lib.sys import Logger
class __BaseSystem:
    # 获取工作目录
    CWDIR = os.getcwd()
    # 运行文件

    _disks = []
    
    logger = Logger("system", "executor.log")

    def _check_soft_status(self, alias, path):
        # 遍历系统进程池
        for process in psutil.process_iter():
            # 匹配项目
            if re.match(alias, process.name()):
                # 匹配名称相同的进程
                if process.exe() == path:
                    yield process
        
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
    
    def close_software(self, software, path):
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
    
    def remove(self, path):
        # 移动文件或删除
        pass
            
    def checkfile(self, check_object, base=None):
        # 查找文件
        results = []
        if base is None:
            # 默认全盘搜索
            base = self._disks
        elif base not in self._disks:
            # 校验非法磁盘
            raise "disk is not exist"
        
        for root, dirs, files in os.walk(base):
            for file in files:
                if file == check_object:
                    results.append(os.path.join(root, file))
            for dir in dirs:
                if dir == check_object:
                    results.append(os.path.join(root, dir))
                    
        return results
    
    def executor(self, args, *,
                 cwd:Path=None,
                 stdin: str=None,
                 timeout:int=None,
                 ):
        """
        :param label: PID标识
        :param args: 封装的shell指令列表
        :return report: 返回报文, 用于向服务端汇报执行结果
        """
        process= subprocess.Popen(
                args=args,
                shell=True, 
                text=True,
                stdin = subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
            )
        msg, err = process.communicate(input=stdin, timeout=timeout)
        return msg, err
    
        
    def report(self, args, msg, err):
        # 格式化报文
        return json.dumps({
            "status": "ok" if not err else "error",
            "instruct": " ".join(args) if isinstance(args, Iterable) else args,
            "msg": msg if msg else "<No output>",
            "err": err if err else "<No error output>",
            "time": time.time()
        }, ensure_ascii=False)   
    
    
    def build_hyperlink(self, alias, frompath):
        pass
    
    def uproot(self):
        # 升级root权限
        pass
    
    
    def format_params(self, typecode:int, data: dict|list) -> str:
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

    
    def record(self, level:int, msg):
        self.logger.record(level, msg)
        # logtext = " ".join(map(str, msg))
        # for other in dmsg:
        #     logtext = "\n" + other + dmsg[other]
        # self.logger.record(1, f"{logtext}")