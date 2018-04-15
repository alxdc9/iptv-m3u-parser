#!/usr/bin/env python3
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import shutil
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
URL = CONFIG.get('Provider', 'URL')

class Handler(http.server.SimpleHTTPRequestHandler):

#     def __init__(self):
#         pass
    FILEPATH = 'sample.txt'

    def do_GET(self):
        print(URL)
        # Construct a server response.
        self.parsedURL = parse_qs(urlparse(self.path).query)

        self.getParameters()

        with open(self.FILEPATH, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-Type", 'application/octet-stream')
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(self.FILEPATH)))
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)

    def getParameters(self):
        """
        Gets username, password and wanted groups
        """
        self.username = self.parsedURL['user'][0]
        self.password = self.parsedURL['pass'][0]
        self.groups = self.parsedURL['groups'][0].split(',')


if __name__ == '__main__':
    
#     Config = ConfigParser.ConfigParser(

    print('Server listening on port 8000...')
    httpd = socketserver.TCPServer(('', 8000), Handler)
    httpd.serve_forever()
