import redis

# 异常捕捉工具箱
class CatchTools:
    def __init__(self):
        self.logs = []
    
    def redis(self, func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except redis.ConnectionError:
                print("无法连接redis")
        return wrapper
    

Catch = CatchTools()