from redis import StrictRedis

from projectdesposetool import CONFIG

REDIS_CONF = CONFIG.parseConfig("redis_config")


class DataBaseManager(StrictRedis):
    def __init__(self, *args, **kwargs):
        super().__init__(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=0, decode_responses=True)
    
    def lrange(self, key, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = self.llen(key)
        return super().lrange(key, 0, end)

    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def init_start(self):
        for data in REDIS_CONF['datas']:
            pass
            
            
DataBaseManager = DataBaseManager()

if __name__ == "__main__":
    print(REDIS_CONF['datas'])