import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from controller import HTTPRequestHandler
if __name__ == '__main__':
    server_address = ('', 8080)
    file_path = sys.argv[1]
    httpd = HTTPServer(server_address, lambda *args, **kwargs: HTTPRequestHandler(*args, **kwargs, file_path=file_path))
    print('Server running...')
    httpd.serve_forever()