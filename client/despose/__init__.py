import os
import json
from xml.etree import ElementTree as et

from despose.parse import CONFIG


def build_directory(path):
    if not os.path.exists(path):
        print(f"make dir {path}")
        os.makedirs(path)
        


class Despose:
    def __init__(self):
        pass
    
    def build_directory(path):
        pass
    
    
    def get_heartpack(self):
        with open(CONFIG.PATH_MAP_SOFTWARES, "r") as f:
            softwares = json.load(f)
            for item in softwares:
                try:    # 初始状态下item可能为None ? 历史问题， 后续可能不需要捕获异常
                    del item['ecdis']['path']
                except KeyError:
                    pass
        return {
            "mac": CONFIG.MAC,
            "ip": CONFIG.IP,
            "softwares": softwares
        }

DESPOSE = Despose()