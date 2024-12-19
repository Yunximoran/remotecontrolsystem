from redis import Redis

from projectdesposetool import CONFIG


REDIS_CONF = CONFIG.parseConfig("redis_config")


RedisConn = Redis(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=0, decode_responses=True)
    
# print(REDIS_CONF.items())