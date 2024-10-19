# Remote Control System Projcet

## Start：启动入口

## Core：核心

* [api模块](Core/api.py)

  * servers/send_control_shell
  * servers/send_software_checklist
  * clients/send_heart_pkgs
* [udp模块](Core/udp.py)

  * UDP

    * async def register(self)
    * async def activate(self)
    * def run(self)
  * Reception

    * async def reception(self)

    ```python
    # 创建接收数据任务
    while True:
        if len(self.CHECK_CONNSTART) > MAXCONNNUM:
            continue
        coroutine = self.__reception()
        self.loop.create_task(coroutine)
    ```

    * async def __reception(self)

    ```python
    # 实现接受数据任务
    rec = self.udp_socket.recvfrom(1024)

    data = rec[0].decode(ENCODING)
    ip, port = rec[1]

    await self.__check_connection(ip, data)

    return data
    ```

    * async def __check_connection(self, ip, data)
      校验客户端的连接状态：

    ```python
    # True 为连接则创建计时器并启动，False 重置计时器
    if ip not in CLIENTSTART:
        timer = self.__timer(ip)
        self.CHECK_CONNECTION[ip] = (True, data, timer)
    else:
        timer = self.CHECK_CONNECTION[ip][2]
        timer.cancel()
    await timer

    ```

    async def __timer(self, ip)[-](Core/udp.py)
    等待3秒后，删除客户端连接
  * Timer: 重构Reception中计时器代码（为完成）(取消)
* ### [control模块](Core/control.py)


  * sendtoclient(): api接口触发后从数据库中提取正在连接的客户端地址
    通过tcp将处理后的shell列表发送至client
* ### tcp模块

## DataBaseTool： 数据库工具

* [redis_conn](DataBaseTool/redisConnector.py)：redis连接器

## DataModels： API数据模型

* heart_pkgs
* software_checklist

## ProjectDesposeTool： 项目工具

* parse：解析config.xml
* start_server：启动项目服务
* communication： 通信模块（未实现）
