from functools import wraps


class _CatchProcess:
    def __init__(self):
        pass
    
    def process(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                return "强制退出"
        return wrapper
    
    
    

