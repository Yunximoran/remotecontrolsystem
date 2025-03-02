
from lib.init._resolver import _Resolver

from pathlib import Path

def Resolver(f) -> _Resolver:
    if Path(f).suffix == ".xml":
        return _Resolver()
    else:
        return None
    
    
if __name__ == "__main__":
    resoler = Resolver(".config.xml")
    print(resoler("redis", "host"))