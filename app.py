# Import the Flask module
from flask import Flask, request, Response, jsonify

# Import the urllib module
from urllib.parse import urlparse

# Create an instance of the Flask class
app = Flask(__name__)

# Define a global variable for the cookie
_U = '1NssJY8JoQgpNNg8fXA66mbbkV5Ev0YAin-YBPurJ69Zsa0gQ-Bq6eINo9NBQ7tam-OM4pykcZqsteI91B6BNM2AgD1XLp8Xy_yL34R2xDEGsb1V-lpIysooyQOlfECAtk_VJRtKUUWLXOI2TLVpfsrqcQhPGF56o56yge4LI11oy7q3K2v2zRSe6c6kpwP6bwtGVJF6cNtmxgzaf0UTEuw; WLS=C=4f32388253816ce8&N=cf03' #cf03

# Define a function to handle CORS requests
def corsify(f):
    # Define a wrapper function
    def wrapper(*args, **kwargs):
        # Call the original function and get the response
        response = f(*args, **kwargs)
        # Define the CORS headers
        cors_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,HEAD,POST,OPTIONS',
            'Access-Control-Max-Age': '86400',
        }

        # Check if the request has the required headers for CORS
        if (
            request.headers.get('Origin') is not None and
            request.headers.get('Access-Control-Request-Method') is not None and
            request.headers.get('Access-Control-Request-Headers') is not None
        ):
            # Add the CORS headers to the response
            response.headers.update({
                **cors_headers,
                'Access-Control-Allow-Headers': request.headers.get(
                    'Access-Control-Request-Headers'
                ),
            })
        # Return the response
        return response
    # Return the wrapper function
    return wrapper

# Define a function to handle WebSocket requests
@corsify
def handle_websocket():
    # If needed, you can replace serverUrl with your server address
    serverUrl = "https://sydney.bing.com"
    # Create a new URL object based on the request URL
    currentUrl = request.url
    # Create a new URL object based on the server URL and the request path and query
    fetchUrl = serverUrl + currentUrl.path + currentUrl.query

    # Create a new request object based on the fetch URL and the request
    serverRequest = request.copy_with(url=fetchUrl)
    # Set the origin and referer headers
    serverRequest.headers['origin'] = 'https://www.bing.com'
    serverRequest.headers['referer'] = 'https://www.bing.com/search?q=Bing+AI'

    # Get the cookie header or an empty string
    cookie = serverRequest.headers.get('Cookie', '')
    # Append the global cookie if it is not already present
    if '_U=' not in cookie:
        cookie += '; _U=' + _U

    # Set the cookie header
    serverRequest.headers['Cookie'] = cookie

    # Fetch the server response
    res =  fetch(serverRequest)
    # Get the data from the server response
    data = res.get_data()
    # Create a new URL object based on the data
    url = data.decode('utf-8')
    # Fetch the response from the URL
    newRes = fetch(url)
    # Create a new response object based on the new response
    newRes = Response(newRes.get_data(), newRes.status_code, newRes.headers)

    # Set the CORS headers
    newRes.headers['Access-Control-Allow-Credentials'] = 'true'
    newRes.headers['Access-Control-Allow-Headers'] = '*'

    # Create a new URL object pointing to http://ipecho.net/plain
    Ipurl = "http://ipecho.net/plain"
    # Fetch the response from that URL
    Ipresponse = fetch(Ipurl)
    # If the response status code is 200, it means success
    if Ipresponse.status_code == 200:
        # Get the response text content
        textip = Ipresponse.get_data(as_text=True)

    # Set the TestLog and Guestip headers
    newRes.headers['TestLog'] = "This is Sydney@" + textip

    # Return the new response
    return newRes

# Define a route for the root path
@app.route('/', methods=['GET', 'HEAD', 'POST', 'OPTIONS'])
# Define a function to handle requests to the root path
@corsify
def fetch():
    # Get the upgrade header
    upgradeHeader = request.headers.get('Upgrade')
    # Check if the upgrade header is websocket
    if upgradeHeader == 'websocket':
        # Call the handle_websocket function
        return handle_websocket()
    # Create a new URL object based on the request URL
    uri = request.url
    # Parse the URL with the urlparse function
    parsed_url = urlparse(uri)
    # Set the hostname to www.bing.com
    hostname = 'www.bing.com'
    # Reconstruct the URL with the new hostname
    new_url = parsed_url._replace(netloc=hostname).geturl()
    # Fetch the response from the new URL
    return fetch(new_url)

# Run the app
if __name__ == '__main__':
    app.run()
