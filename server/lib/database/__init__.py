

from .redis.connector import Connector as Redis
from .mysql.workbench import WorkBench as MySQL

# 默认的数据库
Redis = Redis()
