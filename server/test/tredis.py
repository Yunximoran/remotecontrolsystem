
from lib.database.redis import Connector
import json
DB = Connector()

c = DB.hgetall("fefe")
print(c, type(c))

