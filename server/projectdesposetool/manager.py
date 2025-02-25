import os
import re
import sys
from pathlib import Path

CWD = Path.cwd()

# 项目管理器
class ProjectManager:
    def __init__(self):
        self.pools = []
        self.processes = []
        self.sockes = []
        self.path = Path(CWD)
    
    def choose_file():
        pass

if __name__ == "__main__":
    pm = ProjectManager()
    s = pm.joinpath("local", "data", "software.json")
    print(s)