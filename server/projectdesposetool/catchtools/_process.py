from functools import wraps, partial

from ._catch import _BaseCatch
from ..systool.logger import Logger


class _CatchProcess(_BaseCatch):
    logger = Logger("process", log_file="process.log")
    
    def process(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.record(func)
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                self.record(func, "The Ctrl C", 3)
                return "强制退出"
        return wrapper
    
    
    
    

