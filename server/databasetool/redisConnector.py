from redis import Redis, StrictRedis

from projectdesposetool import CONFIG
# import aioredis


REDIS_CONF = CONFIG.parseConfig("redis_config")


class DataBaseManager(StrictRedis):
    def __init__(self, *args, **kwargs):
        super().__init__(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=0, decode_responses=True)
    
    def lrange(self, name, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = self.llen(name)
        return super().lrange(name, 0, end)
            
DataBaseManager = DataBaseManager()

    
    # def hset(self, table, target, data):
    #     # return super().hsetnx
    
# print(REDIS_CONF.items())