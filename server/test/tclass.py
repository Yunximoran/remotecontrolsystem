class A:
    def __init__(self):
        self.a = 1
    
    def get(self):
        return self.a

class B(A):
    def __init__(self):
        self.b = 0
        
b = B()

print(b.get())