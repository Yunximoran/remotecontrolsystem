import os
import re
import json
import redis
from redis import StrictRedis

from projectdesposetool import CONFIG
from projectdesposetool.catchtools import Catch

REDIS_CONF = CONFIG.parseConfig("redis_config")



class DataBaseManager(StrictRedis):
    def __init__(self, *args, **kwargs):
        super().__init__(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=0, decode_responses=True)
    
    def status(self):
        try:
            self.ping()
            return True
        except redis.ConnectionError:
            return False
    
    
    def lrange(self, key, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = self.llen(key)
        return super().lrange(key, 0, end)

    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def init_start(self):
        """
            启动初始化
        """
        for data in REDIS_CONF['datas']:
            pass
        
    @Catch.redis
    def execute_command(self, *args, **options):
        return super().execute_command(*args, **options)
    
    
    @Catch.redis
    def dump(self, tbn, ft):
        with open(f"data/{tbn}.json", 'w', encoding="uft-8") as f:
            if ft == "dict":
                datas = self.hgetall(tbn)
            
            if ft == "list":
                datas = self.lrange(tbn)
            json.dump(datas, f)
    
    @Catch.redis
    def load(self):
        workdir = os.getcwd()
        for child in os.listdir(os.path.join(workdir, "data")):
            if os.path.isfile(child):
                # 获取表名
                tbn = child.split(".")[0]
                with open(child, "r") as f:
                    datas = json.load(f)
                    if isinstance(datas, dict):
                        for k in datas:
                            self.hset(tbn, k, datas[k])
                    
                    if isinstance(datas, list):
                        for d in datas:
                            self.lpush(tbn, d)
                            

            
            
DataBaseManager = DataBaseManager()