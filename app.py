from flask import Flask, Response, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'WellCome! Site is working ......'

@app.route('/<path:subpath>')
def proxy(subpath):
    resp = requests.request(
        method=request.method,
        url='https://sydney.bing.com/' + subpath,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    app.run(port=7860)
