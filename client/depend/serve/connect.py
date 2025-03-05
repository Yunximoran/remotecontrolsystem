from ._base import *
class ConnectServe(BaseServe):
    def serve(self):
        # 每秒广播心跳包数据
        udp_conn = BroadCast()
        while True:
            time.sleep(1)
            heart_pkgs = self.get_heartpack()
            udp_conn.send(json.dumps(heart_pkgs))   
        
    def get_heartpack(self):
        with open(PATH_MAP_SOFTWARES, "r") as f:
            softwares = json.load(f)
        return {
            "ip": IP,
            "mac": MAC,
            "softwares": softwares
        }