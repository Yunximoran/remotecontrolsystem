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
            
            
DataBaseManager = DataBaseManager()