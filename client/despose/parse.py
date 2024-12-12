from xml.etree import ElementTree as et

class Parse:
    def __init__(self) :
        self.__TREE = et.parse("config.xml")
        self.__ROOT = self.__TREE.getroot()
        
        self.message()
        
        self.load_connect_config()
        self.load_pathconfig()
        self.load_buildconfig()
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
        
        self.PATH_LOG_SHELLS = self.__PATHROOT.find("log_shells").text
        self.PATH_MAP_SOFTWARES = self.__PATHROOT.find("map_softwares").text
    
    def load_buildconfig(self):
        BUILDROOT = self.__ROOT.find("build")
        STRUCTURE = BUILDROOT.find("structure")
        self.LOCAL_DIR_ROOT = STRUCTURE.get('target')
        self.LOCAL_DIR_DATA = "\\".join([self.LOCAL_DIR_ROOT, STRUCTURE.findall("dir")[0].text])
        self.LOCAL_DIR_LOGS = "\\".join([self.LOCAL_DIR_ROOT, STRUCTURE.findall("dir")[1].text])
        self.LOCAL_DIR_SOFTWARES = "\\".join([self.LOCAL_DIR_ROOT, STRUCTURE.findall("dir")[2].text]) 
        
        self.ENCODING = BUILDROOT.find("encoding").text     
    
    def load_performance(self):
        self.__PERFORMANCE = self.__ROOT.find("performance")
        
        self.MAXPROCESS = int(self.__PERFORMANCE.find("max_process").text)

        
CONFIG = Parse()
if __name__ == "__main__":
    print(CONFIG.LOCAL_DIR_SOFTWARES)
    print(CONFIG.ENCODING)

