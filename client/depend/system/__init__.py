from .linux import Linux
from .windows import Windows
from .macos import MacOS
from ._base import __BaseSystem

from lib import Resolver


resolver = Resolver()

OS = resolver("computer", "os")

def System(**kwargs) -> __BaseSystem:
    if OS == "Windows":
        return Windows(**kwargs)
    elif OS == "Linux":
        return Linux(**kwargs)
    elif OS == "MacOS":
        return MacOS(**kwargs)
    else:
        raise "系统标识错误"

SYSTEM = System()