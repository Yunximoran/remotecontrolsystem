# 使用Python 3.11版本的基础镜像
FROM python:3.11

# 安装Node.js和npm
RUN apt-get update && apt-get install -y nodejs npm && apt-get clean

# 安装Redis
RUN apt-get update && apt-get install -y redis-server && apt-get clean

# 将当前目录下的所有文件添加到镜像的/Server目录中
ADD . /Server

# 设置工作目录为/Server
WORKDIR /Server

# 安装Python项目依赖
RUN pip install -r requirements.txt

# 设置工作目录为/Server/view
WORKDIR /Server/view

# 安装前端项目依赖
RUN npm install

# 构建前端项目
RUN npm run build

# 设置工作目录回/Server
WORKDIR /Server

# 暴露Python应用运行的端口
EXPOSE 3000

# 启动Redis服务器和Python应用
CMD ["sh", "-c", "redis-server /Server/databasetool/redis-service.conf & python start.py"]
