#!/usr/bin/env python3
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import shutil
import configparser
import urllib.request

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')
URL = CONFIG.get('Provider', 'URL')

class Handler(http.server.SimpleHTTPRequestHandler):

    FILEPATH = 'sample.txt'

    def do_GET(self):

        # Parses request
        self.parsedURL = parse_qs(urlparse(self.path).query)

        # Gets parameters out of request
        self.getParameters()

        self.url = self.getUserURL()

        self.downloadm3u()

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

    def getUserURL(self):
        url = URL
        usernameString = 'username=' + self.username
        passwordString = 'password=' + self.password

        url = url.replace('username=', usernameString)
        url = url.replace('password=', passwordString)

        return url

    def downloadm3u(self):
        # Downloads file from provider
        response = urllib.request.urlopen(self.url)
        self.m3uContent = response.readlines()
        del self.m3uContent[0]
        print(self.m3uContent[0].decode('utf-8'))

    def createList(self):
        pass


if __name__ == '__main__':
    
#     Config = ConfigParser.ConfigParser(

    print('Server listening on port 8000...')
    httpd = socketserver.TCPServer(('', 8000), Handler)
    httpd.serve_forever()
