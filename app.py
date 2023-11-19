from flask import Flask, request, Response
import requests

app = Flask(__name__)

# 定义一个代理函数，用于向目标服务器发送请求
def proxy(url, method, headers, data):
    # 设置Origin头部为https://www.bing.com
    headers['Origin'] = 'https://www.bing.com'
    # 根据请求方法发送相应的请求
    if method == 'GET':
        r = requests.get(url, headers=headers, stream=True)
    elif method == 'POST':
        r = requests.post(url, headers=headers, data=data, stream=True)
    else:
        # 其他方法暂不支持
        return Response(status=200)
    # 返回一个响应对象，保留原始响应的状态码和头部
    return Response(r.content, status=r.status_code, headers=r.headers.items())

# 定义一个路由，用于处理根路径的请求
@app.route('/')
def index():
    # 返回一个简单的消息
    return 'WellCome! Site is working ......'

# 定义一个路由，用于处理其他路径的请求
@app.route('/<path:path>')
def other(path):
    # 获取请求的完整URL，替换主机名为sydney.bing.com
    url = request.url.replace(request.host, 'sydney.bing.com')
    # 获取请求的方法，头部和数据
    method = request.method
    headers = request.headers
    data = request.data
    # 调用代理函数，返回响应
    return proxy(url, method, headers, data)

# 运行Flask应用，监听7860端口
if __name__ == '__main__':
    app.run(port=10000, debug=True)
