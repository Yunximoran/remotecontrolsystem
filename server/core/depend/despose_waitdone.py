from databasetool import DataBaseManager as DATABASE
from core.depend.protocol.tcp import TCPConnect

class Despose:
    def __init__(self):
        while True:
            result = DATABASE.hget("waitdone_despose_results")    # 保存ip地址和
            conn = TCPConnect()
            
    
        