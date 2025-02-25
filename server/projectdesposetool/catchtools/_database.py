import inspect
from typing import Annotated, Callable
from functools import wraps

from redis import ConnectionError

from ._catch import _BaseCatch
from ..systools.logger import Logger



class _CatchDatabase(_BaseCatch):
    logger = Logger("database", log_file="database.log")
    def __init__(self):
        pass
    
    def redis(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.record(func)
                return func(*args, **kwargs)
            except ConnectionError:
                self.record(func, "无法连接Redis", 3)
                return "无法连接redis"
        return wrapper