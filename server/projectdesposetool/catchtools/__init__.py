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

    def process(self, tasks=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except KeyboardInterrupt:
                    print("正在热重启")
                    if task:
                        for task in tasks:
                            task.terminate()
                            task.join()
                    return False
            return wrapper
        return decorator
    
    def pool(self, pool):
        print(pool)
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    # value
    
    
Catch = _CatchTools()