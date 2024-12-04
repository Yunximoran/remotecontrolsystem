import os
import subprocess
import time
import pickle
import inspect


class M:
    def s(cls):
        return inspect.getsource(cls)
    


print(M.__name__)