from http.server import BaseHTTPRequestHandler
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, MenuController):
        self.controller = MenuController

    def do_GET(self):
        self.controller.handle_request(self)

    def do_POST(self):
        self.controller.handle_request(self)