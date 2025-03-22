from lib.init.resolver import __resolver
from pathlib import Path

path = __resolver("logs")
db = path.search("db")
print(db.path)
