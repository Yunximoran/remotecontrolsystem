import sys
import redis
from functools import wraps, partial

# 异常捕捉工具箱
class _CatchTools:
    def __init__(self):
        self.logs = []
    
    def redis(self, func):
        # redis相关错误
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except redis.ConnectionError:
                print("无法连接redis")
                return False
        return wrapper

    def asyncloop(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            loop, sock = func(*args, **kwargs)
            try:    # 事件循环
                loop.run_forever()
            finally:
                loop.close()
                sock.close()
        return wrapper

    def process(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                print("强制退出")
        return wrapper
    
    def pool(self, pool):
        print(pool)
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    
Catch = _CatchTools()