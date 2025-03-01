from __future__ import annotations
from typing import List, AnyStr, Generator
from xml.etree.ElementTree import Element

class Node:
    def __init__(self, node:Element, parent:Node = None):
        self.tag = node.tag
        self.attrib = node.attrib
        self.parent = parent
        self.data = None
        
        self.__size = 0
        self.__childs:List[Node] = []
        
        
        if parent is not None:
            self.addr = parent.addr.copy()
        else:
            self.addr = []
        
        self.addr.append(self.tag)

    
    def addchild(self, node):
        self.__size += 1
        self.__childs.append(node) 
           
    def search(self, *tags):
        """
            pass
        """
        current = self
        for tag in tags:
            current = current.__search(tag)
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
    
    def __iter__(self) -> Generator[Node, None, None]: 
        for elem in self.__childs:
            yield elem
    
    def __str__(self) -> AnyStr:
        return f"{self.tag}: {self.data}" if self.data else self.tag
    
    def __len__(self):
        return self.__size
