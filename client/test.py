import os
import subprocess
import time
import pickle


for i in []:
    print(type(i), i)
    
    
class S:
    def __init__(self):
        pass
    
    def count(self, n, b):
        return n * b
    
with open("software_.pkl", "wb") as f:
    pickle.dump(S(), f)
    
    

with open("software_.pkl", "rb") as f:
    s = pickle.load(f)
    

print(s.count(1, 3))