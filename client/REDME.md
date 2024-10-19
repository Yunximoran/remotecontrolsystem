# Main

* 实现通过UDP广播心跳包

# Protocol 实现UDP和TCP协议

* 实现UDP单播机制
* 实现UDP广播机制
* 新增select进程模块监听tcp连接，获取数据
  * 处理连接数据，得到shell列表
  * 交由run_shell方法统一执行
* 新增check_software方法检查本地进程获取软件清单运行状态

# Init 初始化

* [ ] 识别操作系统
