from multiprocessing import Process
from multiprocessing.process import BaseProcess
from multiprocessing.pool import Pool
import sys
try:
    from ..parse import CONFIG
    from ..catchtools import Catch
except ImportError:
    from projectdesposetool.parse import CONFIG
    from projectdesposetool.catchtools import Catch

# RemoteProcess
class MultiPool(Pool):
    def __init__(self, processes = None, initializer = None, initargs = (), maxtasksperchild = None, context = None):
        if processes is None or processes < 5:
            processes = CONFIG.MINPROCESS   # 5  
        elif processes > 10:
            processes = CONFIG.MAXPROCESS   # 10
        super().__init__(processes, initializer, initargs, maxtasksperchild, context)
    
    def map_async(self, func, iterable, chunksize=None, callback=None, error_callback=None):
        return super().map_async(func, iterable, chunksize, callback, error_callback)
    
    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        return super().apply_async(func, args, kwds, callback, error_callback)
    
    @Catch.pool
    def worker(self, func, *args, **kwargs):
        func()
    
    """
    step0: 对任务进行包装， 触发Key异常时的捕获
    
    """
    
    
    
    # 尽量不使用with
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.join()

    

class MultiProcess(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon = None):
        # super().__init__(group, target, name, args, kwargs, daemon=daemon)
        super().__init__(group, name=name, daemon=daemon)
        self._target = self._worker
        self._args = (target, )
        self._kwargs = {
            "args": args,
            "kwargs": kwargs
        }

    def start(self):
        return super().start()
    
    @Catch.process
    def _worker(self, func, args=(), kwargs={}):
        print(func)
        return func(*args, **kwargs)
    
    def join(self, timeout = None):
        try:
            return super().join(timeout)
        except KeyboardInterrupt:
            pass
    