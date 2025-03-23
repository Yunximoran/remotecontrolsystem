from functools import wraps

class A:
    
    def status(self, param):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(param)
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    
a = A()

@a.status("hello")
def td():
    print("world")
    
td()