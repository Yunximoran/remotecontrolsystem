import inspect
from typing import Annotated, Callable


from ..systool.logger import Logger



# 基础Catch，定义所有Catch类公共属性
class _BaseCatch:
    logger = Logger("latest", log_file="latest.log")
    def __init__(self):
        pass
    
    @staticmethod
    def getlogtext(func: Callable, msg):
        return f"""callable: {func.__name__}
        path: {inspect.getabsfile(func)}
        from: {func.__module__}
        message:{msg}
        """
    
    def log_level(self, level: int) -> Callable:
        if level == 0:
            return self.logger.info
        
        elif level == 1:
            return self.logger.debug
        
        elif level == 2:
            return self.logger.warning
        
        elif level == 3:
            return self.logger.error
        
        elif level == 4:
            return self.logger.critical