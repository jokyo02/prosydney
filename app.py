# 导入Flask和Requests库
from flask import Flask, request, Response
import requests

# 创建一个Flask应用
app = Flask(__name__)

# 定义一个路由，匹配所有的请求
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    # 获取用户的请求方法、URL、头部和数据
    method = request.method
    url = 'https://sydney.bing.com/' + path
    headers = dict(request.headers)
    data = request.data or request.form or None
    
    # 修改origin头部为https://www.bing.com
    #headers['host'] = 'sydney.bing.com'
    headers['origin'] = 'https://www.bing.com'
    
    # 发送请求给https://sydney.bing.com，并获取响应
    response = requests.request(method, url, headers=headers, data=data)
    
    # 创建一个Response对象，将响应的状态码、头部和内容返回给用户
    return Response(response.content, response.status_code, response.headers.items())

# 运行Flask应用
if __name__ == '__main__':
    app.run()
