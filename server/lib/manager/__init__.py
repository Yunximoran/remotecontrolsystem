from ._logger import Logger
from ..init.resolver import __resolver
from ..init.exception import RESOLVERERROR

class Manager:
    def __init__(self):
        pass
    
    
    def setdb(self, db, option, value, isattr=False):
        dbc = __resolver("database")
        if not db in dbc:
            raise RESOLVERERROR(f"option {db} is not exist")
        else:
            dbc = dbc.search(db)
            
        if isattr:
            dbc.setattrib(option, value)
        else:
            option = dbc.addelement(option, value)
            if not option.data == value:
                option.setdata(value)