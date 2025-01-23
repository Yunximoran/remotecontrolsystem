from multiprocessing import Process
from multiprocessing.pool import Pool


from ..parse import CONFIG
from ..catchtools import Catch

# RemoteProcess
class MultiPool(Pool):
    def __init__(self, processes = None, initializer = None, initargs = (), maxtasksperchild = None, context = None):
        if processes is None:
            processes = CONFIG.MINPROCESS   # 5  
        elif processes > 10:
            processes = CONFIG.MAXPROCESS   # 10
        super().__init__(processes, initializer, initargs, maxtasksperchild, context)
        
    @Catch.process
    def map_async(self, func, iterable, chunksize = None, callback = None, error_callback = None):
        return super().map_async(func, iterable, chunksize, callback, error_callback)
    
    @Catch.process
    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        return super().apply_async(func, args, kwds, callback, error_callback)
    
    
    """
    step0: 对任务进行包装， 触发Key异常时的捕获
    
    """
    @Catch.pool
    def wrapper(self, func, *args, **kwargs):
        return func(*args, **kwargs)
    
    def test(self):
        self.terminate()
        self.join()
        self.close() 
    
    def catch(func):
        def wrapper(self, *args, **kwargs):
            pass
        return wrapper
    
    
    
    # 尽量不使用with
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.join()
    
    """
    pool
    while 
        res = pool.apply_async
        res.get
    
    catch:
        terminate
        join
    finally:
        close
        join
    
    """
    

class MultiProcess(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        
        
    @Catch.process
    def start(self):
        return super().start()
    
    def terminate(self):
        return super().terminate()
    



def ps():
    while True:
        print("ps")

if __name__ == "__main__":
    p = MultiProcess(target=ps, args=())
    p.start()