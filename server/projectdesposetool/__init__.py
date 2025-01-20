import os
import sys


from .parse import CONFIG
from .systool import choose_file

# 项目管理器
class ProjectManage:

    def __init__(self):
        pass
        

    def registry(self, action, *args):
        self.pool.map(action, *args)
    
    @staticmethod
    def loaddata(db):
        workdir = os.getcwd()
        for child in os.listdir(os.path.join(workdir, "data")):
            if os.path.isfile(child):
                tbn = os.path.basename(child)
                with open(child, "r") as f:
                    datas = f.readlines()
                    for data in datas:
                        item = data.strip().split("\t")
                        db.hset(tbn, item[0], item[1])
    
    @staticmethod
    def savedata(db, key):
        try:
            datas = db.hgetall(key)
        except Exception:
            datas = db.lrange(key)
        workdir = os.getcwd()
        with open(os.path.join(workdir, f"data/{key}.txt"), 'w') as f:
            if isinstance(datas, dict):
                for k in datas:
                    f.write(f"{k}\t{datas[k]}\n")
            else:
                for data in datas:
                    f.write(f"{data}\n")
                
    def shutdown(self):
        sys.exit()        
    



