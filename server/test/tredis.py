from lib.database import Redis


db = Redis()

keys = db.keys()

print(keys)