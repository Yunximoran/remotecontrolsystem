from typing import Annotated, Callable
import inspect
from functools import wraps
from ._database import _CatchDatabase
from ._process import _CatchProcess
from ._socket import _CatchSock

from ..systool.logger import Logger

class _CatchTools(
        _CatchDatabase, 
        _CatchProcess,
        _CatchSock
    ):
    logger = Logger("catch", log_file="sys.log")
    def __init__(self):
        self.logs = []
    
    # 默认捕获器
    def catch(self, *args, **kwargs):
        """
            额外的日志说明
        log attr:
            instruct: "sudo apt update"
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    self.record(func, 0)
                    return func(*args, **kwargs)
                except Exception:
                    return False
                except KeyboardInterrupt:
                    self.record(func, "The Ctrl C Single is teriggered", 3)
                    return False
                finally:
                    return None
            return wrapper
        return decorator
    
    def timeout(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.record(func)
                return func(*args, **kwargs)
            except TimeoutError:
                self.record(func, "Timeout", 3)
                return False
        return wrapper
    

    
    
    def __close__(self):
        for close in self.CLOSE:
            close.close()

    

