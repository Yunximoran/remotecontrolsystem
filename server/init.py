from lib import Resolver
from lib.sys import NetWork


def init():
    resolver = Resolver()
    net = NetWork("WLAN")
    
    root = resolver.root
    netnode = root.addelement("network")
    netnode.addelement("ip", text=net.IPv4)
    netnode.addelement("mac", text=net.mac)
    resolver.save()
    
if __name__ == "__main__":
   init() 


