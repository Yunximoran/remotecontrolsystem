from lib.init.resolver import __resolver


db = __resolver("database")
print("redis" in db)