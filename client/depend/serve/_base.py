import json
import time
import os
import multiprocessing



from lib import Resolver
from lib.sys import Logger
from depend.protocol import TCPListen, TCPConnect
from depend.protocol import BroadCast, MultiCast
from depend.path import (
    LOCAL_DIR_FILE,
    PATH_LOG_SHELLS,
    PATH_MAP_SOFTWARES
)
from depend.system import SYSTEM

resolver = Resolver()
IP = resolver("network", "ip")
MAC = resolver("network", "mac")
class BaseServe:
    def __init__(self):
        self.serve()
    
    def serve(self):
        pass