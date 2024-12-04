import os
from xml.etree import ElementTree as et

from despose.parse import CONFIG

def checkfile(file, basedir):
    # 在指定目录中查找文件 -> 文件绝对路径
    for root, _, files in os.walk(basedir):
        if file in files:
            return os.path.join(root, file)
    
    return None
