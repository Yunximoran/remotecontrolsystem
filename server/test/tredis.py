
from lib.database.redis import Connector
import json
DB = Connector()

c = DB.hgetall("heart_packages")


json.loads(None)