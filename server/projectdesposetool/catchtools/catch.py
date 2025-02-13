from typing import Annotated
from functools import wraps
from ._database import _CatchDatabase
from ._process import _CatchProcess
from ._socket import _CatchSock

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
                return func(*args, **kwargs)
            except Exception:
                return False
            except KeyboardInterrupt:
                return "The Ctrl C Single is triggered"
            finally:
                return None
        return wrapper
    
    
    def timeout(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TimeoutError:
                return "Timeout"
        return wrapper
    
    
    def __close__(self):
        for close in self.CLOSE:
            close.close()

    
    
