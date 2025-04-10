from pathlib import Path

from lib import Resolver

res = Resolver()
res = res("path", "local")
local = res.bind(Path.cwd())
items = [item for item in local.rglob("Clash.zip") if item.is_file()]
print(items[0])
