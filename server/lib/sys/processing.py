from functools import partial
from multiprocessing import Process as _Process
from multiprocessing.pool import Pool as _Pool
from multiprocessing import (
    Lock,
    Queue,
    Value,
)

from lib.init.resolver import __resolver
from lib.catch import _CatchProcess


Catch = _CatchProcess()


@Catch.process
def worker(func, *args, **kwargs):
    """
        包装工作函数
    func: 目标函数
    args: 函数实参元组
    kwargs: 函数实参字典
    """
    return func(*args, **kwargs)

# 获取进程输出信息
def stdout(res):
    print(res)
    
# 获取进程错误信息
def stderr(err):
    print(err)


class Pool(_Pool):
    
    def __init__(self, processes = None, initializer = None, initargs = (), maxtasksperchild = None, context = None):
        """
            初始化进程池
        定义进程数范围
        """
        if processes is None or processes < 5:
            processes = __resolver("preformance", "min-processes") 
        elif processes > 10:
            processes = __resolver("preformance", "max-processes")
        super().__init__(processes, initializer, initargs, maxtasksperchild, context)
        
    def map_async(self, func, iterable, chunksize = None, callback = None, error_callback = None):
        _worker = partial(worker, func)
        return super().map_async(_worker, iterable, chunksize, callback, error_callback)

    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        _worker = partial(worker, func)
        return super().apply_async(_worker, args, kwds, callback, error_callback)

    def join(self):
        try:
            return super().join()
        except KeyboardInterrupt:
            self.terminate()

    

class Process(_Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon = None):
        super().__init__(group, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._target = partial(worker, target)
    
    def start(self):
        return super().start()
    
    def run(self):
        return super().run()
    
    def join(self, timeout = None):
        try:
            return super().join(timeout) 
        except KeyboardInterrupt:
            self.terminate()