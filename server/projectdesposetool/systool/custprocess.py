from multiprocessing import Process
from multiprocessing.pool import Pool


class MultiPool(Pool):
    def map_async(self, func, iterable, chunksize = None, callback = None, error_callback = None):
        return super().map_async(func, iterable, chunksize, callback, error_callback)
    
    def apply_async(self, func, args=(), kwds={}, callback=None, error_callback=None):
        return super().apply_async(func, args, kwds, callback, error_callback)
    

class MultiProcess(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)



def ps():
    while True:
        print("ps")

if __name__ == "__main__":
    p = MultiProcess(target=ps, args=())
    p.start()