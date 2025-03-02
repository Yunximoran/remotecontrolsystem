import re
from pathlib import Path

from typing import List, AnyStr, ByteString
from xml.etree import ElementTree as et
from xml.etree.ElementTree import Element

try:
    from .__node import Node
except ImportError:
    from lib.init.__node import Node
    
    
WORKDIR = Path.cwd()
CONFPATH = WORKDIR.joinpath("lib", "init", ".config.xml")
ENCODING = "utf-8"


    
class XML:
    def __init__(self, file=CONFPATH):
        self.__conf = et.parse(file)
        self.__root = self.__conf.getroot()
    
        self.root = self.deep(self.__root)
    
    def save(self):
        # 设置缩进
        et.indent(self.__conf, space="\t", level=0)
        # 写入修改
        self.__conf.write(CONFPATH) 
        
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
    
    def __encoding(self, context: AnyStr | ByteString, encoding=ENCODING)\
        -> AnyStr | ByteString:
        # 编码转换器
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


def Resolver(file=CONFPATH) -> XML:
    # 解析器，根据不同的文件类型返回对应的解析器
    if type(file) != Path:
        file = Path(file)
    if not file.exists():
        raise Exception(f"文件不存在: {file}")
    
    if re.match("^\.(xml)$", file.suffix):
        return XML(file)
    elif re.match("^\.(ya?ml)$", file.suffix):
        print("yaml")
    elif re.match("^\.(ini)$", file.suffix):
        print("ini")
    elif re.match("^\.(json)$", file.suffix):
        print("json")
    else:
        raise Exception("文件格式错误")
    
    
if __name__ == "__main__":
    p = Resolver()