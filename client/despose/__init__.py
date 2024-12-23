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
        return {
            "mac": CONFIG.MAC,
            "ip": CONFIG.IP,
            "softwares": softwares
        }

DESPOSE = Despose()