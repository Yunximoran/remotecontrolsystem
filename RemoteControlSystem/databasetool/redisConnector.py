from redis import Redis, ConnectionPool

from projectdesposetool import Parse


REDIS_CONF = Parse.parseConfig("redis_config")


RedisConn = Redis(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=0)


class RedisTools:
    def __init__(self) -> None:
        self.conn = ConnectionPool()
    

if __name__ == "__main__":
    RedisConn.pubsub()

    
    