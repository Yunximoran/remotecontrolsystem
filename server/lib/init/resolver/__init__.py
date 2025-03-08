from ._resolver import *


def Resolver(file=PUBLICCONF):
    return _Resolver(file)

_resolver = _Resolver(PRIVATECONF)