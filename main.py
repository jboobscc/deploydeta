import re
import requests

from flask import Flask
from flask import request
from flask import Response

from werkzeug import LocalProxy

from ws4py.client.geventclient import WebSocketClient

app = Flask(__name__)
app.debug = True

PROXY_DOMAIN = "127.0.0.1:8888"
PROXY_FORMAT = u"http://%s/%s" % (PROXY_DOMAIN, u"%s")
PROXY_REWRITE_REGEX = re.compile(
    r'((?:src|action|[^_]href|project-url|kernel-url|baseurl)'
    '\s*[=:]\s*["\']?)/',
    re.IGNORECASE
)
websocket = LocalProxy(lambda: request.environ.get('wsgi.websocket', None))
websockets = {}


class WebSocketProxy(WebSocketClient):
    def __init__(self, to, *args, **kwargs):
        self.to = to
        print(("Proxy to", self.to))
        super(WebSocketProxy, self).__init__(*args, **kwargs)

    def opened(self):
        m = self.to.receive()
        print("<= %d %s" % (len(m), str(m)))
        self.send(m)

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
        print("=> %d %s" % (len(m), str(m)))
        self.to.send(m)

methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH",
           "CONNECT"]


@app.route('/proxy/', defaults={'url': ''}, methods=methods)
@app.route('/proxy/<path:url>', methods=methods)
def proxy(url):
    with app.test_request_context():
        if websocket:
            while True:
                data = websocket.receive()
                websocket_url = 'ws://{}/{}'.format(PROXY_DOMAIN, url)
                if websocket_url not in websockets:
                    client = WebSocketClient(websocket_url,
                                             protocols=['http-only', 'chat'])
                    websockets[websocket_url] = client
                else:
                    client = websockets[websocket_url]
                client.connect()
                if data:
                    client.send(data)
                client_data = client.receive()
                if client_data:
                    websocket.send(client_data)
            return Response()
    if request.method == "GET":
        url_ending = "%s?%s" % (url, request.query_string)
        url = PROXY_FORMAT % url_ending
        resp = requests.get(url)
    elif request.method == "POST":
        if url == 'kernels':
            url_ending = "%s?%s" % (url, request.query_string)
            url = PROXY_FORMAT % url_ending
        else:
            url = PROXY_FORMAT % url
        resp = requests.post(url, request.data)
    else:
        url = PROXY_FORMAT % url
        resp = requests.request(url, request.method, request.data)
    content = resp.content
    if content:
        content = PROXY_REWRITE_REGEX.sub(r'\1/proxy/', content)
    headers = resp.headers
    if "content-type" in headers:
        mimetype = headers["content-type"].split(";")[0].split(",")[0]
    else:
        mimetype = None
    response = Response(
        content,
        headers=dict(headers),
        mimetype=mimetype,
        status=resp.status_code
    )
    return response
proxy.provide_automatic_options = False
