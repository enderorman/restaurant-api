from http.server import BaseHTTPRequestHandler, HTTPServer
from controller import HTTPRequestHandler
if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print('Server running...')
    httpd.serve_forever()