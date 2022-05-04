from io import BytesIO
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi
import http.server
import ssl

""" Simple SSL server """


# creating the keyfile:
# openssl req -new -x509 -keyout localhost.pem -out localhost.pem -days 365 -nodes

class requestHandler(BaseHTTPRequestHandler):

    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self.set_headers()

    def do_GET(self):
        self.set_headers()
        server_test = {'greet': 'hello world', 'received': 'ok'}
        test_json = json.dumps(server_test)
        test_json = bytes(test_json, 'utf-8')
        self.wfile.write(test_json)

    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers.get('content-type'))
        if content_type != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        content_length = int(self.headers.get('content-length'))
        content = self.rfile.read(content_length).decode('utf-8')
        content_json = json.loads(content) if content else None

        self.set_headers()
        #self.wfile.write(content_json.encode('utf-8'))


def server_conn(server_class=HTTPServer, handler_class=requestHandler, port=4443):
    try:
        httpd = http.server.HTTPServer(('localhost', port), handler_class)
        httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='localhost.pem',
                                       ssl_version=ssl.PROTOCOL_TLS)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print('shutting down server')
        # httpd.close()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        server_conn(port=int(argv[1]))

    else:
        server_conn()
