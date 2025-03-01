from pathlib import Path
from .init._resolver import _Resolver, WORKDIR


# 项目管理器
class Manager:
    def __init__(self):
        self.pools = []
        self.processes = []
        self.sockes = []
        self.path = Path(WORKDIR)
        
        
    def Pool(self):
        """
            管理
        """
        pass


