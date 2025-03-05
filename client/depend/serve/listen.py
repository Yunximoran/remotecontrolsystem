from ._base import *

class ListenServe(BaseServe): 
    # 监听组播端口， 获取软件清单  
    def serve(self):
        multi_conn = MultiCast()    # 激活组播端口
        pool = multiprocessing.Pool()
        while True:
            data = multi_conn.recv()
            softwares = json.loads(data) # 解析服务端软件清单
            # pool.map_async(self._update_softwares, softwares)
            # 为每次接收到的软件清单创建处理进程
            print(softwares)
            newitem = []
            with open(PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
                local_softwares: list[dict] = json.load(f)
                for item in softwares:
                    itemname = item['ecdis']['name']
                    isexist = False
                    for localitem in local_softwares:
                        localname = localitem['ecdis']['name']
                        if itemname == localname:
                            isexist = True
                            break
                    if not isexist:
                        newitem.append(item)
                
            pool.map_async(self._update_softwares, newitem, callback=self._write_local_softwares)
            
    def _update_softwares(self, softwares):
        # 更新软件清单
        software_name = softwares['ecdis']['name']
        print("software name", software_name)
        allpath = SYSTEM.checkfile(software_name)
        print("all path:", allpath)
        params = SYSTEM.format_params(1, allpath)
        resp = self._wait_response(params)
        print("results:", resp)
        softwares['ecdis']['path'], report = SYSTEM.build_hyperlink(software_name, resp)
        self._report_results(report)
        return softwares

     
    def _write_local_softwares(self, nvals):
        lcoal_softwares: list[dict]= json.load(open(PATH_MAP_SOFTWARES, 'r'))
        lcoal_softwares.extend(nvals)
        json.dump(lcoal_softwares, open(PATH_MAP_SOFTWARES, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        print("save ok")
            
    def _report_results(self, report):
        conn = TCPConnect()
        SYSTEM.format_params(2, report)
        conn.send(SYSTEM.format_params(2, report))
        conn.close()
        del conn
        
    def _wait_response(self, param):
        conn = TCPConnect()
        conn.send(param)
        data = conn.recv()
        conn.close()
        return data.decode()
