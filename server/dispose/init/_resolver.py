import re
from pathlib import Path

from typing import List, AnyStr, ByteString
from xml.etree import ElementTree as et
from xml.etree.ElementTree import Element

try:
    from .__node import Node
except ImportError:
    from dispose.init.__node import Node
    
    
WORKDIR = Path.cwd()
CONFPATH = WORKDIR.joinpath("despose", "init", ".config.xml")
ENCODING = "utf-8"


class _Resolver:
    def __init__(self, file=CONFPATH):
        # xml et只能find到下一级标签
        conf = et.parse(file)
        self.__root = conf.getroot()
        self.root = self.deep(self.__root)
    
    def deep(self, root: Element, parent: Node = None) -> Node:
        """
            解析器
        返回字典数据
        node: 解析开始节点
        addr: 节点所在位置，如果为空列表则表示从根节点开始
        """
        node = Node(root, parent)
        # print(node.addr)
        if len(root) == 0:
            node.data = self.__type_conversion(root.text)
        else:
            list_data = self.__list_options(root)
            if list_data != []:
                # 确保li元素不会被深入
                # print(list_data)
                node.data = list_data
            else:
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
    
    def __type_conversion(self, context: AnyStr) -> int|float|str:
        if re.match("^\d+$", context):
            return int(context)
        elif re.match("^[-+]?(\d*\.\d+)$", context):
            return float(context)
        elif re.match("^[\t\n]$", context):
            return None
        else:
            return context

    def __encoding(self, context: AnyStr | ByteString, encoding=ENCODING)\
        -> AnyStr | ByteString:
        # 编码转换器
        try:
            return context.encode(encoding)
        except AttributeError:
            return context.decode(encoding)
    
    def __call__(self, *args):
        node = self.root.search(*args)
        return node.data

  
    
    


