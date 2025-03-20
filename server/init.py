from lib import Resolver
from lib.init.resolver import __resolver
from lib.sys import NetWork
import time, re
resolver = Resolver()

NET = NetWork("WLAN")
CORS = [
    "https://127.0.0.1:8080",
    "http://127.0.0.1:8080"
]
PASSWORD = {
    "computer": "ranxi160259"
}
_PASSWORD = {
    "mysql": "redis",
    "redis": "123465"
}

def setpassword():
    for option in PASSWORD:
        conf = resolver(option)
        conf.setattrib('password', PASSWORD[option])

    for option in _PASSWORD:
        conf = __resolver(option)
        conf.setattrib('password', _PASSWORD[option])
    
        
def setnetwork():
    net = resolver("network")
    ip = net.search("ip")
    mac = net.search("mac")
    
    if not ip:
        net.addelement("ip", text=NET.IPv4)
    else:
        ip.settext(NET.IPv4)
        
    if not mac:
        net.addelement("mac", text=NET.mac)
    else:
        mac.settext(NET.mac)

def setcors():
    server = resolver("server")
    cors = server.search('cors')
    if cors:
        for item in CORS:
            try:
                cors.push(item)
            except Exception:
                continue
            

def close():
    resolver.save()
    __resolver.save()

def init():
    setcors()
    setnetwork()
    setpassword()
    close() 



if __name__ == "__main__":
    init()
    
    


