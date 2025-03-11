class A:
    def __init__(self, a):
        self.__a = a
        
    def itera(self):

        for i in self.__a:
            print(i)
            
            

class B(A):
    def __init__(self):
        self.__a = []
        super().__init__(self.__a)
        
    
    def add_a(self, i):
        self.__a.append(i)
        
    
        
        
    
    
b = B()

b.add_a(1)
b.add_a(2)

b.itera()