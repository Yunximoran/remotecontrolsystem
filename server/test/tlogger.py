


class A:
    def pa(self):
        a = 3
        def pa2():
            print(a)
        return pa2
        

a1 = A()
a1.pa()()