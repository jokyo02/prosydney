# 导入Flask和Requests库
from flask import Flask, request, Response
import requests
# 导入random库，用于生成随机数
import random

# 创建一个Flask应用
app = Flask(__name__)

# 定义一个函数，生成随机字符串
# 参数 e 是字符串的长度，默认为 32
def randomString(e=32):
    # 定义一个字符串，包含所有可能的字符
    t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678_-+"
    # 初始化一个空字符串，用于存储结果
    n = ""
    # 循环 e 次，每次从 t 中随机选择一个字符，拼接到 n 中
    for i in range(e):
        n += t[random.randint(0, len(t) - 1)]
    # 返回 n
    return n

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
    headers['origin'] = 'https://www.bing.com'

    # 获取请求头中的 Cookie 字段，如果没有则为空字符串
    cookie = request.headers.get('Cookie', '')
    cookies = cookie

    # 如果 Cookie 中没有 KievRPSSecAuth 字段，就添加一个随机字符串
    if 'KievRPSSecAuth=' not in cookie:
        cookies += '; KievRPSSecAuth=' + randomString(512)

    # 如果 Cookie 中没有 _RwBf 字段，就添加一个随机字符串
    if '_RwBf=' not in cookie:
        cookies += '; _RwBf=' + randomString(256)

    # 如果 Cookie 中没有 MUID 字段，就添加一个随机字符串
    if 'MUID=' not in cookie:
        cookies += '; MUID=' + randomString(32)

    # 如果 Cookie 中没有 _U 字段，就添加一个随机字符串
    if '_U=' not in cookie:
        cookies += '; _U=' + randomString(128)

    # 设置新的请求头中的 Cookie 字段为 cookies
    headers['Cookie'] = cookies
    
    # 发送请求给https://sydney.bing.com，并获取响应
    response = requests.request(method, url, headers=headers, data=data)
    
    # 创建一个Response对象，将响应的状态码、头部和内容返回给用户
    return Response(response.content, response.status_code, response.headers.items())

# 运行Flask应用
if __name__ == '__main__':
    app.run()
