from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

class NEATHTTPServer(HTTPServer):

    def __init__(
            self,
            server_address,
            request_handler,
            bind_and_activate=False):
        super().__init__(
        server_address,
            request_handler,
            bind_and_activate
        )

class NEATHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self):
        super().__init__(re, cli, serv)

class NEATServer(object):


    def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
        server_address = ('', 8000)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()