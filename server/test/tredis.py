from lib.database import Redis


db = Redis()

db.delete("1.1.1.1")
print(db.get("1.1.1.1"), type(db.get("1.1.1.1")))

# db.delete("1.1.1.1")