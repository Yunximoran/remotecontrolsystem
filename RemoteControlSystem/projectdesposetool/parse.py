try:
    import os
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



class Parse:
    def __init__(self) -> None:
        self.CWD = os.getcwd()
        self.CONF = ET.parse("\\".join([self.CWD, "config.xml"]))
        self.ROOT = self.CONF.getroot().find("list")


    def parseConfig(self, TAG):
        RES = {}
        
        s = self.ROOT.find(TAG)
        for elem in s:
            RES[elem.tag] = elem.text

        return RES