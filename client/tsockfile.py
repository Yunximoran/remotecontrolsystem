from lib.sys.system import SYSTEM
from pathlib import Path

from lib.sys.system import linux


a = linux.Linux()
a.compress(r"E:\test", r"D:\workbench\remotecontrolsystem\client\lib", "gz")
# a = Path("he.tar.gz")
# print(a.stem)