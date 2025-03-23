import json

from depend.path import *

with open(PATH_MAP_SOFTWARES, "r", encoding="utf-8") as f:
    print(json.load(f))