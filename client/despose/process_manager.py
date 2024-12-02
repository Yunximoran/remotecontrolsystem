import multiprocessing
from .parse import CONFIG

MAXPROCESS = 10 # "CONFIG.MAXPROCESS"

class ProcessManager:
    def __init__(self):
        self.pool = multiprocessing.Pool(processes=MAXPROCESS)
        

PROCESSMANAGER = ProcessManager()