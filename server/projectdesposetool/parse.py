try:
    import os
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



class Parse:
    def __init__(self) -> None:
        self.init()
        self.load_allconfig()
        
    def init(self):
        self.CWD = os.getcwd()
        self.CONF = ET.parse("/".join([self.CWD, "config.xml"]))
        self.ROOT = self.CONF.getroot().find("base")
        
        self.IP = self.ROOT.get("ip")

    def load_allconfig(self):
        self.loadconnect()
        self.loadredis()
        self.loadservers()


    def loadconnect(self):
        CONNECT = self.ROOT.find('connect')
        UDPCONN = CONNECT.find("udp")
        TCPCONN = CONNECT.find("tcp")
        
        self.UCPORT = int(UDPCONN.find('client').text)
        self.USPORT = int(UDPCONN.find('server').text)
        self.UBPORT = int(UDPCONN.find("broad").text)
        self.UMPORT = int(UDPCONN.find("multi").text)
        
        self.TCPORT = int(TCPCONN.find("client").text)
        self.TSPORT = int(TCPCONN.find('server').text)
    
    def loadredis(self):
        REDISCONN = self.ROOT.find("redis_config")
        
        self.RHOST = REDISCONN.find("host").text
        self.RPORT = int(REDISCONN.find("port").text)
    
    def loadservers(self):
        SERVERS = self.ROOT.find("servers")
        
        self.UVICORNSERVER = SERVERS.find("uvicorn").text
        self.LISTENINGSERVER = SERVERS.find("listening").text
        self.CONTROLSERVER = SERVERS.find("control").text
        self.REDISSERVER = SERVERS.find("redis").text


    def parseConfig(self, TAG):
        RES = {}
        
        s = self.ROOT.find(TAG)
        for elem in s:
            RES[elem.tag] = elem.text

        return RES
    
CONFIG = Parse()

