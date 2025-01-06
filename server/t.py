class T:
    def __init__(self):
        self.tttt = 0
    
    #decorator
    @staticmethod
    def p(func):
        def wapper(self, *args, **kwargs):
            print("hello world")
            self.tttt += 1
            res = func(self, *args, **kwargs)
            return res
        return wapper
    
    @p
    def Tt1(self, x, y):
        
        return x * y
    
t = T()
res = t.Tt1(1, 2)
print(res)
print(t.tttt)