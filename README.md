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
  * ## RemoteControlSystem/emulating_server.py	: 模拟server运行

    * api_server: 模拟server触发send_shell请求
    * udp_server: 模拟server启动udp监听client连接
    * 测试结果：同时启动api_server和udp_server，运行正常。
* ### 2024-10-22：

  * ## server：


    * 新增view前端部分，实现触发api接口向client发送数据
    * 新增MultiCast模块，实现触发api接口后向client发送软件清单
  * ### client：


    * 新增listen服务，监听server发送的软件清单，保存至data/software.json
    * 新增find_software功能，从软件名称获取软件所在地址
    * init.py功能暂定

      * [X] 安装client时，获取本机信息（ip, mac, system)，初始化config.xml
      * [ ] 封装多个操作系统，保存需要的不同系统下常用的shell指令，统一调用方法
  * ### RemoteControlSystem/emulatin_server.py:


    * api_server: 新增模拟组播发送软件清单
  * ### run project

    1、运行remotecontrolsystem/start.py 启动api、control、udp进程

    2、运行client/main.py 启动客户端

    3、进入remotecontrolsystem/view 终端： npm run serve (view启动服务未完成， 需要另外启动)
