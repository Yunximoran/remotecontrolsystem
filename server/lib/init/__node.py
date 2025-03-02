from __future__ import annotations
import re
from typing import List, AnyStr, Generator
from xml.etree.ElementTree import Element, SubElement
"""
    
    
    
    
"""
class Node:
    def __init__(self, node:Element, parent:Node = None):
        self.tag = node.tag         # 节点名
        self.attrib = node.attrib   # 节点包含属性
        self.parent = parent        # 节点父元素
        self.data = self.__retype(node.text)

        self.__node = node              # 原始Element对象
        self.__size = 0                 # 子元素数量
        self.__childs:List[Node] = []   # 子元素列表
        
        # 设置当前节点所在位置
        if parent is not None:
            self.addr = parent.addr.copy()
        else:
            self.addr = []
        self.addr.append(self.tag)
        
        self.level = len(self.addr)
        
    def type(self):
        if self.data is None:
            return "tag"
        else:
            return "val"
    
    def setdata(self, data):
        # 对数据进行转换并设置为data属性
        self.data = self.__retype(data)
        
    def addchild(self, node):
        # 添加子元素
        self.__size += 1
        self.__childs.append(node)
    
    def getelement(self) -> Element:
        # 获取原始Element
        return self.__node
    
    def addelement(self, tag, text="\n", attrib = {}, **extra) -> Node:
        # 如果子节点已存在，返回子节点
        fount = self.search(tag)
        if fount is not None and abs(fount.level - self.level) == 1:
            return fount
        
        # 创建新Element
        newelem = SubElement(self.__node, tag, attrib, **extra)
        # 设置默认文本， 没有设置会成为单标签文件报错
        newelem.text = text + "\t" *len(self.addr) if text == "\n" else text
        
        # 生成新Node， 绑定父Node为self
        newnode = Node(newelem, self)
        # 绑定子Node为新Node
        self.__childs.append(newnode)
        
        # 返回新Node， 执行一些额外测操作，如设置文本，设置属性，修改标签名等
        return newnode
    

        
    def delelement(self, node):
        # 从子元素中找到目标Node
        if node in self.__childs:
            # 删除相关引用
            self.__childs.remove(node)
            self.__node.remove(node.getelement())
        else:
            # 否则报错目标Node不是当前Node的子元素
            raise ValueError("node not in childs")
    
     
    def setattrib(self, key, val):
        # 为当前元素设置属性，并同步Node属性
        self.__node.set(key, str(val))
    
    def delattrib(self, key):
        # 删除当前元素的某个属性，并同步Node属性
        if key in self.attrib.keys():
            del self.__node.attrib[key]
        else:
            raise KeyError(f"{self}not attribute {key}")
            
    def search(self, *tags) -> Node:
        # 创建指针，只想当前节点
        current = self
        for tag in tags:
            # 遍历标签， 逐级定位到指定节点
            current = current.__search(tag)
            # 如果为空，定位错误，返回None
            if current is None:
                break
        return current
    

           
    def __search(self, tag) -> Node:
        
        if self.tag == tag:
            return self
        else:
            for next in self.__childs:
                res = next.__search(tag)
                if res is not None:
                    return res
            return None
        
    def __retype(self, context: AnyStr) -> int|float|str:
        """
            对数据进行转换
        """
        if re.match("^\d+$", context):
            return int(context)
        elif re.match("^[-+]?(\d*\.\d+)$", context):
            return float(context)
        # elif re.match("^[\t.*\n]$", context):
        elif re.match("^[(true)|(yes)|1]$", context):
            return True
        elif re.match("^[(false)|(no)|0]$", context):
            return False
        elif re.match("^[\t\n]+$", context):
            return None
        else:
            return context 
            
    def __iter__(self) -> Generator[Node, None, None]:
        for elem in self.__childs:
            yield elem
    
    def __str__(self) -> AnyStr:
        return f"{self.tag}: {self.data}" if self.data else self.tag
    
    def __len__(self):
        return self.__size
