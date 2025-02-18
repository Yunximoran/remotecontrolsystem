from projectdesposetool.systool.processing import Pool, Process
# from multiprocessing import Pool
from projectdesposetool.catchtools import Catch

import time
def t(x, t=1):
    while True:
        print(x, t)


def e(err):
    print(err)
    
def testpool(obj):
    # with MultiPool() as pool:
        pool = Pool()
        if obj == "map":
            pool.map_async(t, ("hello", "world", "1", "2", "3", "4"), error_callback=e)
            
        elif obj == "apply":
            for i in range(10):
                pool.apply_async(t, ("world",), kwds={"t": i}, error_callback=e)

        pool.close()
        pool.join()
        
def testprocess():
    Process(target=t, args=("world",), kwargs={"t": 3,}).start()
    
def deep():
    Process(target=testpool, args=("apply", )).start()
if __name__ == "__main__":
    deep()