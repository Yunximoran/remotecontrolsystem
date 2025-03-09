from functools import wraps, partial

from ._catch import __CatchBase, Logger


class _CatchProcess(__CatchBase):
    logger = Logger("process", log_file="process.log")
    def process(self, func):
        @wraps(func)
        def wrapper(target, *args, **kwargs):
            try:
                attr:dict = kwargs['attr']
                for key in attr:
                    setattr(target, key, attr[key])
                del kwargs['attr']
            except KeyError:
                pass
            
            try:
                self.record(target)
                return func(target, *args, **kwargs)
            except KeyboardInterrupt:
                self.record(target, "The Ctrl C", 3)
                return False
            # except AttributeError as e:
            #     self.record(func, e)
            #     return False
        return wrapper
    
    
    
    

