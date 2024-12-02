from xml.etree import ElementTree as et

class Parse:
    def __init__(self) :
        self.__TREE = et.parse("config.xml")
        self.__ROOT = self.__TREE.getroot()
        
        self.message()
        
        self.load_connect_config()
        self.load_pathconfig()
        self.load_performance()
    
    def message(self):
        self.IP = self.__ROOT.get("ip")
        self.MAC = self.__ROOT.get("mac")        

    
    def load_connect_config(self):
        self.__CONNECT = self.__ROOT.find("connect")
        
        self.UDPCONF = self.__CONNECT.find("udp")
        self.UBPORT = int(self.UDPCONF.find("broadcast").text)
        self.UMPORT = int(self.UDPCONF.find("multicast").text)
        self.UCPORT = int(self.UDPCONF.find("client").text)
        self.USPORT = int(self.UDPCONF.find("server").text)
        
        self.TCPCONF = self.__CONNECT.find("tcp")
        self.TCPORT = int(self.TCPCONF.find("client").text)
        self.TSPORT = int(self.TCPCONF.find("server").text)        

    def load_pathconfig(self):
        self.__PATHROOT = self.__ROOT.find("paths")
        
        self.PATH_SOFTWARES = self.__PATHROOT.find("path_softwares").text
        
    
    def load_performance(self):
        self.__PERFORMANCE = self.__ROOT.find("performance")
        
        self.MAXPROCESS = int(self.__PERFORMANCE.find("max_process").text)

        
CONFIG = Parse()
if __name__ == "__main__":
    print(CONFIG.IP)

