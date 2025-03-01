from functools import wraps
# from redis import ConnectionError

from ._catch import _Catch, Logger




class _CatchDatabase(_Catch):
    logger = Logger("database", log_file="database.log")
    def __init__(self):
        pass
    
    def ping(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionError:
                return "无连接"
        
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
    