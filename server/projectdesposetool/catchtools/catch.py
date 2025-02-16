from typing import Annotated, Callable
import inspect
from functools import wraps
from ._database import _CatchDatabase
from ._process import _CatchProcess
from ._socket import _CatchSock
from ..systool.logger import Logger

logger = Logger("catch", log_file="sys.log")
class _CatchTools(
        _CatchDatabase, 
        _CatchProcess,
        _CatchSock
    ):

    def __init__(self):
        self.logs = []
        # self.func = func
    
    # 默认捕获器
    def catch(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.__log_record(func, "success", 0)
                return func(*args, **kwargs)
            except Exception:
                return False
            except KeyboardInterrupt:
                self.__log_record(func, "The Ctrl C Single is teriggered", 3)
                return "The Ctrl C Single is triggered"
            finally:
                return None
        return wrapper
    
    
    def timeout(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.__log_record(func, "success", 0)
                return func(*args, **kwargs)
            except TimeoutError:
                self.__log_record(func, "Timeout", 3)
                return "Timeout"
        return wrapper
    
    def __log_record(self, func: Callable, msg, level=0):
        logtext = self.getlogtext(func, msg)
        if level == 0:
            logger.info(logtext)
        
        elif level == 1:
            logger.debug(logtext)
            
        elif level == 2:
            logger.warning(logtext)
        
        elif level == 3:
            logger.error(logtext)
        
        elif level == 4:
            logger.critical(logtext)
    
    def __close__(self):
        for close in self.CLOSE:
            close.close()

    
    
