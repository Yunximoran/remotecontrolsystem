import sys
import redis
import os
import signal
from functools import wraps
from ._database import _CatchDatabase
from ._process import _CatchProcess

class _CatchTools(_CatchDatabase, _CatchProcess):
    def __init__(self):
        self.logs = []
    
    # 默认捕获器
    def catch(func):
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

    
    
