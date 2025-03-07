from ._base import *
from lib.sys import Logger

logger = Logger("ListenServer", "listen.log")
class ListenServe(BaseServe): 
    # 监听组播端口， 获取软件清单  
    def serve(self):
        # 服务入口
        # 加载组播插件
        multi_conn = MultiCast() 
        
        # 创建进程池
        pool = multiprocessing.Pool()
        while True:
            # 接受组播数据： 软件清单
            data = multi_conn.recv()
            # 使用json格式加载数据
            softwares = json.loads(data)
            
            # 更新本地软件清单
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
                        newitem.append(item)
                        
            # 保存更新后的数据
            pool.map_async(self._update_softwares, newitem, callback=self._write_local_softwares)
            
    def _update_softwares(self, softwares):
        # 更新软件清单
        software_name = softwares['ecdis']['name']
        
        # 全盘搜索软件所在位置，获取所有匹配项目
        allpath = SYSTEM.checkfile(software_name)
        # 格式化表单
        params = SYSTEM.format_params(1, allpath)
        # 建立TCP连接服务器，发送匹配列表，等待服务器回应,后去实际地址
        softwares['ecdis']["prac-path"] = self._wait_response(params)
        # 解析服务器回应结果，保存软件位置，并建立软链接
        softwares['ecdis']['path'], report = SYSTEM.build_hyperlink(software_name, softwares['ecdis']["prac-path"])
        # 汇报结果
        self._report_results(report)
        
        # 返回修改后的清单
        return softwares

     
    def _write_local_softwares(self, nvals):
        # 保存json数据
        lcoal_softwares: list[dict]= json.load(open(PATH_MAP_SOFTWARES, 'r'))
        lcoal_softwares.extend(nvals)
        json.dump(lcoal_softwares, open(PATH_MAP_SOFTWARES, 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        logger.record(1, "softwarelist is updated")
            
    def _report_results(self, report):
        # 汇报结果
        # 创建TCP连接
        conn = TCPConnect()
        # 格式化汇报表单
        params = SYSTEM.format_params(2, report)
        # 发送汇报结果
        conn.send(params)
        # 回收TCP占用
        conn.close()
        del conn
        
    def _wait_response(self, param):
        # 等待返回结果
        # 创建TCP连接
        conn = TCPConnect()
        # 发送数据
        conn.send(param)
        # 等待服务器回应
        data = conn.recv()
        # 回收TCP占用
        conn.close()
        return data.decode()
