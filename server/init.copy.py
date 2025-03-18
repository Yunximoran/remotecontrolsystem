from lib.manager import Manager

redispw = None  # 设置redis密码
network = None

datas = []

class Init:
    def __init__(self):
        self.manager = Manager()
        
    def init_database(self):
        if redispw:
            self.manager.setdb("redis", "password", redispw, isattr=True)
            
        if len(datas) > 0:
            self.manager.setdb