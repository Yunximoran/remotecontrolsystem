import os
import pickle
from xml.etree import ElementTree as et

from despose.parse import CONFIG
from despose.process_manager import PROCESSMANAGER



def checkfile(file, basedir):
    # 在指定目录中查找文件 -> 文件绝对路径
    for root, _, files in os.walk(basedir):
        if file in files:
            return os.path.join(root, file)
    
    return None

def loadmodel(file):
    # 加载模块 * pkl ->  类对象
    with open(file, "rb") as f:
        model = pickle.dump(f)
    return model


# DATA MODEL
class SOFTWARE:
    def __init__(self, item):
        self.ecdis = None
        self.conning = None
        
    @property
    def name(self):
        pass 

class ECDIS:
    def __init__(self, name, version, path):
        self.name = name
        self.version = version
        self.path = path
        
    
    def __call__(self, *args: os.Any, **kwds: os.Any) -> os.Any:
        pass
        
