from __future__ import annotations
import re
from pathlib import Path
from typing import List, AnyStr, Any, Generator, Dict, Union
from xml.etree.ElementTree import Element, SubElement
"""
    
"""

class _Node:
    # 类操作
    def __init__(self, tag, node:Element, 
                 parent: Node|PathNode,
                 childs: List[Node|PathNode],
                 level: int,
                ):
        self.tag = tag
        self.parent=parent
        self.level = level    
        
         
        self.__node = node
        self.__childs = childs  

            
    def __iter__(self) -> Generator[Union[Node, PathNode], None, None]:
        for elem in self.__childs:
            yield elem
    
    def type(self):
        # 获取节点类型，[树节点、结构节点， 列表节点， 选项节点]
        if isinstance(self, Node):
            if self.data is None:
                return "tree"
            elif isinstance(self.data, list):
                return "list"
            else:
                return "val"
        elif isinstance(self, PathNode):
            return "struct"
        elif isinstance(self, ItemsNode):
            return "items"
        else:
            raise f"type node error, {self}"
        
    def search(self, *tags) -> Node|PathNode:
        # 创建指针，只想当前节点
        current = self
        for tag in tags:
            # 遍历标签， 逐级定位到指定节点
            current = current._search(tag)
            # 如果为空，定位错误，返回None
            if current is None:
                break
        return current

    def _search(self, tag) -> Node|PathNode:
        if self.tag == tag:
            return self
        else:
            for next in self.__childs:
                res = next._search(tag)
                if res is not None:
                    return res
            return None
    
    def setattrib(self, key, val):
        # 为当前元素设置属性，并同步Node属性
        self.__node.set(key, str(val))
    
    def delattrib(self, key):
        # 删除当前元素的某个属性，并同步Node属性
        if key in self.__node.attrib.keys():
            del self.__node.attrib[key]
        else:
            raise KeyError(f"{self}not attribute {key}")
    
    def addelement(self, tag, text="\n", attrib = {}, **extra) -> Node:
        # 如果子节点已存在，返回子节点
        # 创建新Element
        newelem = SubElement(self.__node, tag, attrib, **extra)
        # 设置默认文本， 没有设置会成为单标签文件报错
        newelem.text = text + "\t" * self.level if text == "\n" else text
        return newelem

    def delelement(self, node: Node):
        self.__node.remove(node.getelement())
        
    def getelement(self) -> Element:
        # 获取原始Element
        return self.__node
    
    def settext(self, text:Any):
        self.__node.text = str(text)
    
    
class Node(_Node):
    def __init__(self, node:Element, parent:Node = None):
        self.tag = node.tag         # 节点名
        self.attrib = node.attrib   # 节点包含属性
        


        # 设置节点数据 
        self.data = self.data = self.__retype(node.text) if node.text is not None else None

        # 设置私有属性
        self.__node = node              # 原始Element对象
        self.__size = 0                 # 子元素数量
        self.__childs:List[Node] = []   # 子元素列表
        
        # 设置节点描述
        if "describe" in node.attrib.keys():
            self.describe = node.attrib["describe"]
        else:
            self.describe = None  
               
        # 设置节点索引
        if parent is not None:
            self.addr = parent.addr.copy()
        else:
            self.addr = []
        self.addr.append(self.tag)    
                   
        super().__init__(
            self.tag,
            node,
            parent,
            self.__childs, 
            len(self.addr)
            )
        

    def setdata(self, data):
        # 对数据进行转换并设置为data属性
        self.data = self.__retype(data)
    
    def settext(self, text):
        if self.type() == "val":
            super().settext(text)
            self.setdata(text)
        else:
            raise "must be a val node to set text"
        
    def addchild(self, node):
        # 添加子元素
        self.__size += 1
        self.__childs.append(node)
    
    
    def addelement(self, tag, text="\n", attrib:Dict = {}, **extra) -> Node:
        # 如果子节点已存在，返回子节点
        fount = self.search(tag)
        if fount is not None and abs(fount.level - self.level) == 1:
            return fount
        
        # 创建新Element
        newelem = super().addelement(tag, text="\n", attrib = {}, **extra)


        # 生成新Node， 绑定父Node为self
        newnode = Node(newelem, self) if "struct" not in attrib.keys() else PathNode(newelem, self)
        

        # 绑定子Node为新Node
        self.__childs.append(newnode)
        
        # 返回新Node， 执行一些额外测操作，如设置文本，设置属性，修改标签名等
        return newnode
        
    def delelement(self, node: Node):
        # 从子元素中找到目标Node
        if node in self.__childs:
            # 删除相关引用
            self.__childs.remove(node)
            self.__node.remove(node.getelement())
        else:
            # 否则报错目标Node不是当前Node的子元素
            raise ValueError("node not in childs")
    
        
    def __retype(self, context: AnyStr) -> int|float|str:
        """
            对数据进行转换
        """
        if re.match("^\d+$", context):
            return int(context)
        elif re.match("^[-+]?(\d*\.\d+)$", context):
            return float(context)
        elif re.match("^[(true)|(yes)|1]$", context):
            return True
        elif re.match("^[(false)|(no)|0]$", context):
            return False
        elif re.match("^[\t\n]+$", context):
            # 只有树节点self.data为空
            return None
        else:
            return context 

    def __str__(self) -> AnyStr:
        type = self.type()
        if type == "struct":
            return f"struct root: {self.tag}"
        if type == "list":
            return "\n".join(self.data)
        if type == "tree":
            return f"node: {self.tag}"
        return f"option {self.tag} :\t{self.data}"
    
    def __getitem__(self, key):
        """
            获取额外的属性数据
        """
        if key == "describe":
            raise "describe is default attribute, plcess get it from the cls"
        if key == "struct":
            raise "struct is safe attribute, plcess get it for the cls"
        return self.attrib[key]

# 特殊节点处理
class PathNode(_Node):
    """
        路径节点
    # attrib包含struct的Element节点为根目录
    从该节点开始解析目录结构
    dir标签表示：子目录 创建子节点
    li标签：表示子文件， 添加进self.files
    
    # 提供关于路径的处理操作
    """

    def __init__(self, node: Element, parent:Node|PathNode):
        """
        tag: 目录名称
        describe: 目录描述
        """
        if parent is None:
            raise "path node must in Node"
        
        self.parent = parent        # 绑定 父目录 [父节点]
        if isinstance(self.parent, Node):
            self.tag = node.tag     # 目录名称
            self.describe = node.attrib['struct']   # 文件描述
            self.path = Path(self.tag)
        else:
            self.tag = node.attrib["name"]  # 目录名称
            self.describe = node.attrib["describe"] if "describe" in node.attrib.keys() else None
            self.path = parent.path.joinpath(self.tag)
            
        # 设置节点索引    
        self.addr = parent.addr.copy()
        self.addr.append(self.tag)            

        
        self.dirs: List[PathNode] =[]
        for dir in node.findall("dir"):
            child = PathNode(dir, self)
            self.dirs.append(child)
        
        # 添加子文件
        self.files: Dict[Path] = {}
        for li in node.findall("li"):
            file_path = self.path.joinpath(li.text)
            self.files[file_path.name] = file_path          

        super().__init__(
            self.tag,
            node, 
            parent,
            self.dirs, 
            level=len(self.addr)
            )
        
    def touch(self, file, isdir=False, isall=False):
        pass
    
    def exits(self):
        pass
    
    def addfiles(self, filename, describe:str=None):
        # 添加文件
        attrib = {}
        if describe:
            attrib["describe"] = describe
            
        self.addelement("li", filename, attrib=attrib)
        
        # 获取节点路径
        newfile = self.path.joinpath(filename)

        # 绑定文件所在目录
        self.files[newfile.name] = newfile
    
    def addchild(self, dirname:str, describe:str=None):
        # 添加目录
        attrib = {
            "name": dirname
        }
        if describe:
            attrib["describe"] = describe
            
        dir = self.addelement("dir", attrib=attrib)  # 创建一个新的Element节点
        dirnode = PathNode(dir, self)
        self.dirs.append(dirnode)
        
        
    def addelement(self, tag, text, describe=None):
        if tag != "dir" or tag != "li":
            raise "pathnode, must a dir or li"
        attrib = {}
        
        # 设置节点描述
        if describe:
            attrib["describe"] = describe
        
        # 创建目录节点
        if tag == "dir":
            attrib['name'] = text
            return super().addelement(tag, attrib=attrib)
        
        # 创建文件节点
        if tag == "li" and not re.match("^[^\\\/]+?\.[^\\\/]+$", text):
            raise "Invalid filename"
        else:
            return super().addelement(tag, text, attrib=attrib)
    
    def setattrib(self, describe):
        # 设置文件描述
        return super().setattrib("describe", describe)
    
    def delattrib(self):
        # 删除文件描述
        super().delattrib("describe")
        
    def settext(self, text):
        return super().settext(text)
    def __str__(self):
        return f"Path: {self.tag}"
    
    def __getitem__(self, key):
        if key in self.files.keys():
            return self.files[key]
        else:
            raise f"there is no such file in directory"

class ItemsNode(Node):
    pass

if __name__ == "__main__":
    from lib import Resolver
    resolver = Resolver()
    datapath = resolver("path", "local")
    addr = datapath.addr
    for dir in datapath:
        print(dir)
