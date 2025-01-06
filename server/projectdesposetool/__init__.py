import multiprocessing
from fastapi import HTTPException

from .parse import CONFIG
from .systool import choose_file

QUEUE = multiprocessing.Queue()


class ProjectManage:
    def __init__(self):
        self.pool = multiprocessing.Pool()
        

    def registry(self, action, *args):
        self.pool.map(action, *args)
    

def CheckLoginInfomation(username, password):
    return True
    # return True if username == "admin" and password == "123456" else False
    

def createid(username, password):
    pass

def findid(username, password):
    pass





