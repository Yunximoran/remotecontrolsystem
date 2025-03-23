from ._base import *
from pathlib import Path
logger = Logger("ListenServer", "listen.log")


class ListenServe(BaseServe): 
    # 监听组播端口， 获取软件清单

    def serve(self):
        print("Listen Serve Started")
        multi_conn = MultiCast()
        pool = multiprocessing.Pool()
        while True:
            # 接受组播数据： 软件清单
            data = multi_conn.recv()
            # 使用json格式加载数据
            softwares = json.loads(data)
            logger.record(1, f"accpet softwarelist: {softwares}")
            newitem = self._check_softwares(softwares)
            # 更新本地软件清单
            pool.map_async(self._update_softwares, newitem, callback=self._write_local_softwares).get()


    def _check_softwares(self, softwares):
        newitem = []
        with open(PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
            # 导入本地软件清单数据
            local_softwares: list[dict] = json.load(f)
            
            # 添加新项目
            for item in softwares:
                itemname = item['ecdis']['name']
                isexist = False
                
                # 如果软件已存在更新/不修改
                for localitem in local_softwares:
                    localname = localitem['ecdis']['name']
                    if itemname == localname:
                        isexist = True
                        break
                # 软件为新软件添加项目
                if not isexist:
                    logger.record(1, f"add new soft {itemname}")
                    newitem.append(item)
        return newitem  
          
    def _update_softwares(self, soft):
        # 更新软件清单
        print("dispose up task")
        software_name = soft['ecdis']['name']
        software_path = Path(soft['ecdis']['path'])
        localpath = SYSTEM.checkfile(software_name, software_path)
        
        if isinstance(localpath, list):
            # 格式化软件表单
            params = SYSTEM.format_params(1, localpath)
            
            # 建立TCP连接服务器，发送匹配列表，等待服务器回应,获取实际地址
            logger.record(1, f"related to {software_name}, path: {localpath}")
            localpath = self.waitpath(params)

        # 创建软连接
        soft['ecdis']['path'], soft['ecdis']['prac-path'], report = SYSTEM.build_hyperlink(software_name, localpath) 
        
        # 汇报结果
        self._report_results(report)
        
        # # 返回修改后的清单
        # self._write_local_softwares(softwares)
        return soft
        

     
    def _write_local_softwares(self, softs):
        # 保存json数据
        print(softs)
        with open(PATH_MAP_SOFTWARES, 'r', encoding='utf-8') as f:
            lcoal_softwares: list[dict]= json.load(f)
            lcoal_softwares.extend(softs)
        
        with open(PATH_MAP_SOFTWARES, 'w', encoding='utf-8') as f:
            json.dump(lcoal_softwares, f, ensure_ascii=False, indent=4)
        logger.record(1, "softwarelist is updated")
            
    def _report_results(self, report):
        # 汇报结果
        # 创建TCP连接
        conn = TCPConnect()
        
        # 格式化汇报表单，并发送汇报结果
        params = SYSTEM.format_params(2, report)
        conn.send(params)

        # 发送完成后回收内存
        conn.close()
        del conn

    def waitpath(self, param:str) -> Path:
        # 等待服务器回应，客户端与服务端交互时使用
        logger.record(1, f"wait resp: {param}")
        conn = TCPConnect()
        # 设置超时时间是30分钟
        conn.sock.timeout(1800)
        # 发送数据
        conn.send(param)
        # 等待服务器回应
        data = conn.recv()
        # 回收TCP占用
        conn.close()
        logger.record(1, f"")
        return Path(data.decode())
