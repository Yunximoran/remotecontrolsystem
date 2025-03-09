from functools import partial, wraps


def t(x, y):
    return x + y

# 这里固定一个参数
s = partial(t, x=3)


def catch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("catch")
        return func(*args, **kwargs)
    return wrapper

@catch
def worker(func, *args, **kwargs):
    """
        包装工作函数
    func: 目标函数
    args: 函数实参元组
    kwargs: 函数实参字典
    """
    return func(*args, **kwargs)

w = partial(worker, func=s)

for i in range(0, 10):
    r = s(y=1)
    print(r)