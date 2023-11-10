from flask import Flask, request, Response
import requests

app = Flask(__name__)

SYDNEY_ORIGIN = 'https://www.bing.com'
KEEP_REQ_HEADERS = [
  'accept',
  'accept-encoding',
  'accept-language',
  'connection',
  'cookie',
  'upgrade',
  'user-agent',
  'sec-websocket-extensions',
  'sec-websocket-key',
  'sec-websocket-version',
  'x-request-id',
  'content-length',
  'content-type',
  'access-control-request-headers',
  'access-control-request-method',
]

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    # Get the target url from the request url
    target_url = SYDNEY_ORIGIN + request.full_path

    # Filter and modify the headers you want
    headers = {}
    for key, value in request.headers.items():
        if key.lower() in KEEP_REQ_HEADERS:
            headers[key] = value
    headers['origin'] = 'https://www.bing.com'
    headers['referer'] = 'https://www.bing.com/search?q=Bing+AI'
   # rand_ip = '163.47.101.101'
   # headers['X-Forwarded-For'] = rand_ip

    cookie = request.headers.get('Cookie') or ''
    cookies = cookie
    if not cookie.startswith('_U='):
        cookies += '; _U=' + ''
    headers['Cookie'] = cookies

    # Send the request to the target url with the modified headers
    response = requests.request(
        request.method,
        target_url,
        headers=headers,
        data=request.get_data(),
        stream=True,
    )

    # Return the response back to the client
    return Response(
        response=response.content,
        status=response.status_code,
        headers=response.headers.items(),
    )
