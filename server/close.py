from databasetool import RedisConn
from projectdesposetool import SERVERMANAGE

RedisConn.close()
SERVERMANAGE.kill()