from lib import Resolver
from lib.sys import NetWork
import time
resolver = Resolver()
class Init:
    def __init__(self):
        self.input_config()
        

        try:
            net = resolver("network")
            ip = net.search("ip")
            mac = net.search("mac")
            
            ip.settext(self.net.IPv4)
            mac.settext(self.net.mac)
        except:
            net = resolver.root.addelement("network")
            net.addelement("ip", text=self.net.IPv4)
            net.addelement("mac", text=self.net.mac)
        "etherent"
        resolver.save()
        
    def input_config(self):
        self.net = NetWork(input("choose net:"))
        
    def input_ports(self):
        pass
    

def init():
    resolver = Resolver()
    net = NetWork("WLAN")
    
    root = resolver.root
    netnode = root.addelement("network")
    netnode.addelement("ip", text=net.IPv4)
    netnode.addelement("mac", text=net.mac)
    resolver.save()
    
    
if __name__ == "__main__":
    Init()

