from lib.sys.processing import MultiPool
import multiprocessing
from functools import partial, wraps

import inspect


# def catch(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print("catch")
#         return func(*args, **kwargs)
#     return wrapper

# @catch
# def worker(func, *args, **kwargs):
#     return func(*args, **kwargs)


def send(ip, d):
    print(ip, d)

ds = [(1, 2), (2, 3), (3, 4), (4, 5)]
ips = ["110222", "2dwwddwd"]
if __name__ == "__main__":
    with MultiPool() as pool:
        sendto = partial(send, d=ds)
        pool.map_async(sendto, ips, attribute={"__name__": send.__name__}).get()
