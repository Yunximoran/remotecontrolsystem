import json
import time
import os
import multiprocessing



from lib import Resolver
from lib.sys.system import *
from lib.manager import Logger
from depend.protocol import TCPListen, TCPConnect
from depend.protocol import BroadCast
from depend.protocol.client_udp import *
from depend.path import (
    LOCAL_DIR_FILE,
    LOCAL_DIR_SOFT,
    PATH_LOG_SHELLS,
    PATH_MAP_SOFTWARES
)

resolver = Resolver()
IP = resolver("network", "ip")
MAC = resolver("network", "mac")
class BaseServe:
    def __init__(self):
        self.serve()

    def serve(self):
        pass