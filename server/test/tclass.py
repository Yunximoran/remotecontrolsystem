class A:
    def __init__(self):
        self.a = 1
        
    def info(self):
        print(self.get())
        
    def get(self):
        return self.a

class B(A):
    def __init__(self):
        self.b = 0
    
    def get(self):
        return 1
        
b = B()

b.info()