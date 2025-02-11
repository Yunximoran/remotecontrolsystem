class _V2:
    def __init__(self):
        self.C = "C"
class _V:
    def __init__(self):
        self.__B = "B"
    
    def sb(self, nv):
        self.__B = nv

    def gb(self):
        return self.__B
    
class V(_V2, _V):
    L = []
    def __init__(self):
        # super().__init__()
        self.A = None
        
    def sb(self, n):
        super().sb(n)
        
    def gb(self):
        return super().gb()
    
    def sA(self):
        print(self.A)

v1 = V()
v2 = V()

v1.sb(3)
print(v1.gb())
# print(v1.L)
# print(v2.L)
# print(V.L)

# s = v1.sA
# s()
# v1.A = 0
# s()