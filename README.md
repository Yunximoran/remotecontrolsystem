# 项目日志

* ## 2024-10-15：

  * # server:

    * 完成对UDP模块的调试
  * # client:

    * 实现心跳包广播机制，尝试使用单播和广播与server进行连接
* ## 2024-10-18：

  * # server：

    * 新增control模块，api接口触发后通过tcp连接client发送shell指令
      * 从 redis 中获取 client address
      * 多进程启动，向所有client发送shell列表
  * ## client：

    * 新增select监听来自server的tcp连接， 获取shell列表
  * ## *** RemoteControlSystem/emulating_server.py	: 模拟server运行

    * api_server: 模拟server触发send_shell请求
    * udp_server: 模拟server启动udp监听client连接
    * 测试结果：同时启动api_server和udp_server，运行正常。
