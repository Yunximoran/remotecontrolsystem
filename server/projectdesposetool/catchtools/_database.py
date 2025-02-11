from functools import wraps

from redis import ConnectionError


class _CatchDatabase:
    def __init__(self):
        pass
    
    def redis(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionError:
                return "无法连接redis"
        return wrapper