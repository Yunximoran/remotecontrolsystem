from functools import wraps

from ._catch import __CatchBase, Logger


class _CatchProcess(__CatchBase):
    logger = Logger("process", log_file="process.log")
    
    def process(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                self.record(args[0])
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                self.record(args[0], "The Ctrl C", 3)
                return "强制退出"
        return wrapper
    
    
    
    

