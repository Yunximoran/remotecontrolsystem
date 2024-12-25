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
        # self.loadservers()


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
    

    def parseConfig(self, TAG):
        RES = {}
        root = self.ROOT.find(TAG)
        # print("type xml", type(root))

        return self.deepparsing(root)

    def deepparsing(self, root:ET.Element):
        tree = {}
        elemnums = len(root)
        if elemnums == 0:
            # tree[root.tag] = root.text
            return root.text
        else:
            for elem in root:
                # tree.append((elem.tag, self.deepparsing(elem)))
                child = self.deepparsing(elem)
                if elem.tag in tree.keys():
                    if isinstance(tree[elem.tag], str):
                         tree[elem.tag] = [tree[elem.tag]]
                    tree[elem.tag].append(child)
                else:
                    tree[elem.tag] = self.deepparsing(elem)
        return tree
        
    
CONFIG = Parse()

