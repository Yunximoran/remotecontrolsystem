# import redis
# import signal
# import os
# import sys
# # from projectdesposetool.systool.custprocess import MultiProcess, MultiPool
import time
import multiprocessing
from functools import wraps


def catch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("process quit")
    return wrapper

@catch
def t2(*args, **kwargs):
    t1(*args, **kwargs)

def t1():
    while True:
        print("hello running")

if __name__ == "__main__":
    pass

    # try:
    #     pool = multiprocessing.Pool(5)
    #     while True:
    #         r = pool.apply_async(t2)
    #         r.get()
    # except KeyboardInterrupt:
    #     pool.terminate()
    #     pool.join()
    # finally:
    #     pool.close()
    #     pool.join()
        


# def worker(task):
#     try:
#         print(f"Processing task {task}")
#         time.sleep(1)
#         print(f"Task {task} completed")
#     except KeyboardInterrupt:
#         # 这里可以添加在子进程中处理中断的代码
#         pass


# if __name__ == '__main__':
#     try:
#         # 创建进程池，设置进程数量为4
#         pool = multiprocessing.Pool(processes=4)
#         tasks = [i for i in range(10)]
#         # 异步执行任务
#         results = [pool.apply_async(worker, args=(task,)) for task in tasks]
        
#         for result in results:
#             result.get()
#         # 关闭进程池，不再接受新的任务
#         pool.close()
#         # 等待所有任务完成
#         pool.join()
#     except KeyboardInterrupt:
#         print("Caught KeyboardInterrupt, terminating workers...")
#         # 终止进程池中的所有进程
#         pool.terminate()
#         # 等待所有进程结束
#         pool.join()
#         print("Workers terminated.")