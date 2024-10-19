"""
    模拟 server
    
step: 启动server， 开始监听udp获取client连接状态
step: 发送shell列表
step: save client heartpackage
step:
"""
import multiprocessing

from core import control
from core import udp

class Server:
    SERVERLIST = []
    def __init__(self):
        self.load_pluging()
        self.start_server()
    
    def api_server(self):
        # api接口被触发后control通过tcp向client发送shell
        
        while True:
            print("enter api server")
            self.controler.sendtoclient("hello this is message from server")
    
    def udp_server(self):
        udp_server = udp.UPD()
        udp_server.run()
    
    def load_pluging(self):
        # 导入插件
        self.controler = control.Control()
        
    def start_server(self):
        # 启动服务端
        udp_server = multiprocessing.Process(target=self.udp_server, args=())
        api_server = multiprocessing.Process(target=self.api_server, args=())
        
        self.SERVERLIST.extend([udp_server, api_server])
        
        
        udp_server.start()
        api_server.start()
        
        for server in self.SERVERLIST:
            server.join()
    

        
    
if __name__ == "__main__":
    Server()