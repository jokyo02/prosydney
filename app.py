from flask import Flask, request, Response
import requests

app = Flask(__name__)

SYDNEY_ORIGIN ='https://testwebing.nbing.eu.org'
#SYDNEY_ORIGIN ='https://www.bing.com'
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
    resp_headers = response.headers.items()
    # Retain the original set-cookies
    resp_headers = [(k, v) for k, v in resp_headers if k.lower() != 'set-cookie']
    #resp_headers.extend([(k, v) for k, v in response.raw.headers.items() if k.lower() == 'set-cookie'])
    #resp_headers = [(k, v.replace('; domain=', '')) for k, v in resp_headers if k.lower() == 'set-cookie']
    for k, v in response.raw.headers.items():
      if k.lower() == 'set-cookie':
        # Remove the domain attribute and its value
        v = v.split(';')
        v = [x for x in v if 'domain' not in x]
        v = ';'.join(v)
        resp_headers.append((k, v))
    return Response(
        response=response.content,
        status=response.status_code,
        headers=resp_headers,
    )
