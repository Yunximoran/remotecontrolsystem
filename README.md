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

* ### 2024-11-1:
  * ### server:
    * 优化控制台页面：
      * 优化shell数据和softwarelist操作接口
        * 新增预览功能
        * 完成控制台数据操作逻辑

      * 新增控制台菜单栏
        * [X]搭建设置选项框架
        * []服务器登录选项(待定)
        * ...(未定)

  * ### version:
    * [X]测试项目linux系统运行
    * [X]增加github版本控制 [main/linux/window]

  * ### run project：
    * init: 
      * start server:
        * install redis
        * install nodejs
        * install vue
          * npm install @vue
          * npm install @vue/cli
        * install python=3.11 fastapi uvicorn redis/redis-py[window/linux]
        * alter server/config.xml: node[base] ip="localhost"
        * run server/start.py
      * start client:
          install python=3.11
          run client/init.py
          run client/main.py

* ### 2024-11-05
  * ### server:
    * ### view:
      * 优化setting option功能
      * 新增client区域，显示client链接状态
      * 新增alter接口
      * 新增data接口
* ### 2024-11-28：
  * ### server:
    * ### view:
      * 进度详情：
      * 基础模块
        * 基本控制按钮
          * [ ] 关闭所有电脑
          * [ ] 开启所有电脑
          * [ ] 重启所有电脑
          * [x] 添加软件
          * [ ] 打开指定软件
          * [ ] 关闭所有软件
          * [ ] 开启所有软件
          * [ ] 下载文件
          * [ ] 批量操作
          * [x] 自定义发送
        * 客户端预览模块
          * 实时监测客户端连接状态
          * 选定发送目标
        * 菜单选项
          * 设置选项：修改config.xml配置
          * 登录选项：注册、 登录账户
        * 日志输出
          * 输出后端交互信息
      * 扩展功能
        * 自定义发送 指令 / 软件清单
      * 优化
        * 引入路由管理(vue-router)
        * 引入状态管理(pinia)
        * 调整整体布局（缩放时存在问题）
    * ### fastapi:
      * 新增account表
        * 保存账户数据
        * 校验登录信息
        * 注册新用户
      * 新增client_status表
      * 更新heart_packages存储
      * 更新send_control_shell接口：
      * 更新软件清单数据模型
      * 更新control与client通信
        * 校验客户端连接状态
        * 默认client_status中正在连接的所有客户端通信
        * 指定与一个或多个客户端进行通信
      * 新增data系列接口： 获取服务端数据
      * 新增alter系列接口： 修改服务端数据，配置文件
  *  ## client:
     * 优化数据存储：
       * json格式
       * 初始化数据表
       * 完成软件清单数据保存
         * 忽略重复项（暂定）=> 可能从服务端修改后再发送，直接保存）

    

