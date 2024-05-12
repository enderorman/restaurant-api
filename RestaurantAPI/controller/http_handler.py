from http.server import BaseHTTPRequestHandler
from controller import MenuController
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, file_path):
        self.file_path = file_path
        super().__init__(request, client_address, server)

    def do_GET(self):
        menuController = MenuController(self.file_path)
        menuController.handle_request(self)

    def do_POST(self):
        menuController = MenuController(self.file_path)
        menuController.handle_request(self)