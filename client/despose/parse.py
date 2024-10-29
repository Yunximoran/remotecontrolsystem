from xml.etree import ElementTree as et

class Parse:
    def __init__(self) :
        self.TREE = et.parse("config.xml")
        self.ROOT = self.TREE.getroot()
        
        self.IP = self.ROOT.get("ip")
        self.MAC = self.ROOT.get("mac")
        
        self.CONNECT = self.ROOT.find("connect")
        
        self.UDPCONF = self.CONNECT.find("udp")
        self.UBPORT = int(self.UDPCONF.find("broadcast").text)
        self.UMPORT = int(self.UDPCONF.find("multicast").text)
        self.UCPORT = int(self.UDPCONF.find("client").text)
        self.USPORT = int(self.UDPCONF.find("server").text)
        
        self.TCPCONF = self.CONNECT.find("tcp")
        self.TCPORT = int(self.TCPCONF.find("client").text)
        self.TSPORT = int(self.TCPCONF.find("server").text)

        
CONFIG = Parse()
if __name__ == "__main__":
    print(CONFIG.IP)

