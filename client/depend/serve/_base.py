import json
import time
import os
import multiprocessing



from lib import Resolver
from lib.sys.system import *
from lib.manager import Logger
from depend.path import (
    LOCAL_DIR_FILE,
    LOCAL_DIR_SOFT,
    PATH_LOG_SHELLS,
    PATH_MAP_SOFTWARES,
    PATH_MAP_FILES
)

resolver = Resolver()
PATH = resolver("local")
IP = resolver("network", "ip")
IP_SERVER = resolver("network", "ip-server")
MAC = resolver("network", "mac")
class BaseServe:
    def __init__(self):
        self.serve()

    def serve(self):
        pass