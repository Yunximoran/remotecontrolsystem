import re
from pathlib import Path

from typing import List, AnyStr, ByteString
from xml.etree import ElementTree as et
from xml.etree.ElementTree import Element

from ._node import Node
    
    
WORKDIR = Path.cwd()
PRIVATECONF = WORKDIR.joinpath("lib", "init", ".config.xml")
PUBLICCONF = WORKDIR.joinpath("lib", ".config.project.xml")
ENCODING = "utf-8"

class _Resolver:
    def __init__(self, file=PRIVATECONF):
        self.__conf = et.parse(file)
        self.__root = self.__conf.getroot()
    
        self.root = self.deep(self.__root)
        
        
    def save(self):
        # 设置缩进
        et.indent(self.__conf, space="\t", level=0)
        # 写入修改
        self.__conf.write(PRIVATECONF)
    
    def annotation(self, node:Element, msg):
        annotated = et.Comment(msg)
        node.append(annotated)
        
    def deep(self, root: Element, parent: Node = None) -> Node:
        """
            解析器
        返回字典数据
        node: 解析开始节点
        addr: 节点所在位置，如果为空列表则表示从根节点开始
        """
        # 创建节点
        node = Node(root, parent)

        # 校验校验是否包含列表数据
        list_data = self.__list_options(root)
        if list_data != []:
            node.data = list_data
        else:
            # 遍历子元素，创建Node绑定父节点为当前节点
            for elem in root:
                next = self.deep(elem, parent=node)
                node.addchild(next)
        return node   
    
    def tohtml(self, node:Element) -> AnyStr:
        # 获取配置文件原始文档
        return self.__encoding(et.tostring(node)) 
          
    def __list_options(self, node:Element) -> List[AnyStr]:
        # 解析列表类型配置
        """
            规定列表数据同一使用li
        并且li元素只具备text属性
        """
        return [li.text for li in node.findall("li")]       
    
    def __encoding(self, context: AnyStr | ByteString)\
        -> AnyStr | ByteString:
        # 编码转换器
        encoding = self.root.search("global", "encoding")
        if encoding is None:
            encoding = "UTF-8"
        try:
            return context.encode(encoding)
        except AttributeError:
            return context.decode(encoding)
    
    def __call__(self, *args):
        node = self.root.search(*args)
        if node is None:
            return None
        else:
            return node if node.data is None else node.data


__all__ = [
    "PRIVATECONF",
    "PUBLICCONF",
    "_Resolver"
]
    