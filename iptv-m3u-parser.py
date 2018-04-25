#!/usr/bin/env python3
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import os
import shutil
import configparser
import urllib.request
import argparse

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


class Parser():


    def filterGroups(self, wantedGroups):    
        output = []
        tag = 'group-title='
        for counter, element in enumerate(self.content):
            index = element.find(tag)
            if index != -1:
                subString = element[index+len(tag)+1:]
                index = subString.find(',')
                group = subString[:index-1]

                if group in wantedGroups:                
                    output.append(element)
                    print(element.find('tvg-name="##########'))
                    if element.find('tvg-name="##########') == -1:
                        print(self.content[counter+1])
                        output.append(self.content[counter+1])            
        
#         for element in output:
#             print(element)


if __name__ == '__main__':    
    
    parser = Parser()
    
    def parseArgs():
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('-f', '--file', action='store_true', help='Sets file mode', default='', required=False)
        parser.add_argument('-g', '--groups', help='groups', default='', required=False)

        return parser.parse_args()

#     Config = ConfigParser.ConfigParser(

    args = parseArgs()
    fileMode = args.file

    if not fileMode:
        print('Server listening on port 8000...')
        httpd = socketserver.TCPServer(('', 8000), Handler)
        httpd.serve_forever()
    
    else:
        groups = args.groups.split(',')
        with open('channels.m3u', 'r') as f:
            parser.content = f.readlines()

        parser.filterGroups(groups)
