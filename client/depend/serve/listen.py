from ._base import *
from pathlib import Path
from lib.sys.sock.udp import BroadCastor

logger = Logger("ListenServer", "listen.log")


class ListenServe(BaseServe): 
    # 监听广播端口， 获取软件清单

    def serve(self):
        print("Listen Serve Started")
        # 绑定指定网卡， 使用port：8083端口
        broadcastor = BroadCastor((IP, LISTENPORT_2))
        pool = multiprocessing.Pool()
        while True:
            # 接收广播数据 -> 软件清单
            data, _ = broadcastor.recv()
            # 使用json格式加载数据
            softwares = json.loads(data)
            logger.record(1, f"accpet softwarelist: {softwares}")
            # newitem = self._check_softwares(softwares)
            
            # 更新本地软件清单
            pool.map_async(
                self._update_softwares, softwares, 
                callback=self._write_local_softwares,
                error_callback=self._PathExistError,
            ).get()

    def _PathExistError(self, err):
        print(err)
        
    def _update_softwares(self, soft):
        # 更新软件清单
        print("dispose up task")
        software_name = soft['ecdis']['name']
        executable = soft['ecdis']['executable']
        software_path = Path(soft['ecdis']['path']).joinpath(executable)
        
        # 检查程序文件是否存在 -> 如果不存在返回可能的路径列表， 否则返回原对象
        localpath = SYSTEM.checkfile(software_name, software_path)
        if isinstance(localpath, list):
            raise "路径不存在"
        
        # 保存实际路径
        soft['ecdis']['prac-path'] = str(localpath)
        
        # 创建软连接： 链接程序路径、报文
        soft['ecdis']['path'], report = SYSTEM.build_hyperlink(LOCAL_DIR_SOFT.joinpath(software_name), localpath) 
        
        # 汇报结果
        self._report_results(report)
        return soft
        
    def _write_local_softwares(self, softs):
        # 保存json数据
        with open(PATH_MAP_SOFTWARES, 'w', encoding=ENCODING) as f:
            json.dump(softs, f, ensure_ascii=False, indent=4)
        logger.record(1, "softwarelist is updated")
        
        new_map_path = set([Path(item['ecdis']['path']) for item in softs])
        old_map_path = set(LOCAL_DIR_SOFT.rglob("*"))

        rmobj = old_map_path - new_map_path
        # 删除多余的项目
        for obj in rmobj:
            obj.unlink()
            
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
        try:
            data = conn.recv()
        except TimeoutError:
            return False
        # 回收TCP占用
        finally:
            conn.close()
        
        return Path(data.decode())
