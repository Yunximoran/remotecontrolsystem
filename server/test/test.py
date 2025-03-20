from lib import Resolver


with Resolver() as r:
    net = r("network")
    print(net.describe)