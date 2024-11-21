import json
from xml.etree import ElementTree as et

from despose.parse import CONFIG



def load_software():
    return json.load(open("data/softwares.json"))
