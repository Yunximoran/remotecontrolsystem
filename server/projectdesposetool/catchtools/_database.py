import inspect
from typing import Annotated, Callable
from functools import wraps

from redis import ConnectionError

from ._catch import _BaseCatch
from ..systool.logger import Logger



class _CatchDatabase(_BaseCatch):
    logger = Logger("database", log_file="database.log")
    def __init__(self):
        pass
    
    def redis(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.__log_record(func, "success", 0)
                return func(*args, **kwargs)
            except ConnectionError:
                self.__log_record(func, "无法连接Redis")
                return "无法连接redis"
        return wrapper
    
    def __log_record(self, func:Callable, msg, level=0):
        logtext = self.getlogtext(func, msg)
        loggin = self.log_level()