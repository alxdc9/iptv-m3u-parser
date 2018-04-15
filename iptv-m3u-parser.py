#!/usr/bin/env python3
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import shutil

class Handler(http.server.SimpleHTTPRequestHandler):

#     def __init__(self):
#         pass
    FILEPATH = 'sample.txt'

    def do_GET(self):
        # Construct a server response.
        self.parsedURL = parse_qs(urlparse(self.path).query)
        
        self.getParameters()
        
        print(self.groups)
        
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
        Gets username and password
        """
        self.username = self.parsedURL['user'][0]
        self.password = self.parsedURL['pass'][0]
        self.groups = self.parsedURL['groups'][0].split(',')


if __name__ == '__main__':

    print('Server listening on port 8000...')
    httpd = socketserver.TCPServer(('', 8000), Handler)
    httpd.serve_forever()