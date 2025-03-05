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
from collections.abc import Iterable
from xml.etree import ElementTree as et
from typing import Tuple
        
class __BaseSystem:
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
