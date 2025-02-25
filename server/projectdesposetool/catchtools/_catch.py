import inspect
from typing import Annotated, Callable


from ..systools.logger import Logger



# 基础Catch，定义所有Catch类公共属性
class _BaseCatch:
    logger = Logger("latest", log_file="latest.log")
    def __init__(self):
        pass
    
    
    def record(self, func, msg="success", level=1):
        logtext = self.logger.format_logtext(func.__name__, msg, module=func.__module__, path=inspect.getabsfile(func))
        self.logger.record(level, logtext)
        
    # def __log_record(self, func, msg="success", level=0):
    #     """
    #     0: debug
    #     1: info
    #     2: waring
    #     3: error
    #     4: critical
    #     """
    #     logtext = logger.format_logtext(func.__name__, msg, model = func.__module__, path = inspect(func))
    #     logger.record(level, logtext)