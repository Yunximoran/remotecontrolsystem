# 远程控制系统客户端部署说明

# 项目依赖
### anaconda3
### python：3.11.10

### 下载项目
```bash
git clone https://github.com//Yunximoran/remotecontrolsystem.git
```

### 运行前准备
#### Linux: 
```bash 安装anaconda3：https://www.anaconda.com/download/success
    Linux: 
    * /bash /path/to/anaconda3-xxxxx-Linux-x86_64.sh
    * sudo vim ~/.bashrc: 最后一行输入: export PATH:/path/to/anaconda3:$PATH
    * source ~/.bashrc
```
#### Windows:
```bash
    * 运行/path/to/anaconda3-xxxxx-Windows-x86_64.exe
```
### 创建虚拟环境
```bash
* conda create -n remotecontrol python=3.11.10
```



### 初始化项目
#### 激活虚拟环境
```bash
  * conda activate remotecontrol
  * conda install -r requirements.txt
```
##### 终端运行
```bash
  * python init.py --ip_server=[服务端IP地址]， --broadcast=[广播域]， --net=[指定网卡名称]
    * python init.py --ip_server=192.168.31.176 --broadcast=192.168.31.255 --net=WLAN
  * python main.py
```


# 设置开机启动

# ！！！ 确保正确修改后在执行
# ！！！ 确保正确修改后在执行
# ！！！ 确保正确修改后在执行
### Linux:
###### ExecStart=__[/path/to/python]__ __[/path/to/client/main.py]__ # 指定python解释器路径，python启动程序
###### WorkingDirectory=__[/path/to/client]__  # 可选：设置工作目录
```bash
# 修改remotecontrol.service 中 [] 
sudo systemctl daemon-reload
sudo systemctl enable remotecontrol.service  # 启用开机自启
sudo systemctl start remotecontrol.service   # 立即启动
```

### Windows:
###### reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run" /v remotecontrol /t REG_SZ /d "\"__[C:\Python39\python.exe\]__" \"__[D:\scripts\script.py\]__"" /f
```bash
# 修改remotecontrol.bat 中 []
运行bat文件
```