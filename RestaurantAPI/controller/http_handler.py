from http.server import BaseHTTPRequestHandler
from controller import MenuController
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        menuController = MenuController()
        menuController.handle_request(self)
    def do_POST(self):
        menuController = MenuController()
        menuController.handle_request(self)