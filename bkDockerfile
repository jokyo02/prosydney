# 使用官方的Ubuntu 22.04镜像作为基础镜像
FROM ubuntu:22.04

# 设置工作目录为/app
WORKDIR /app

# 将当前目录下的所有文件复制到/app目录下
COPY . /app

# 安装Python 3和pip
RUN apt-get update && apt-get install -y python3 python3-pip

# 安装Flask和Requests库
RUN pip3 install flask requests

# 安装Gunicorn
RUN pip3 install gunicorn

# 设置环境变量FLASK_APP为proxy.py
ENV FLASK_APP=app.py

# 暴露8080端口
EXPOSE 7080

# 运行Gunicorn服务器，绑定0.0.0.0:8080，指定proxy:app为应用入口
CMD ["gunicorn", "-b", "0.0.0.0:7080", "app:app"]
