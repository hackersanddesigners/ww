#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import ssl
import urlparse
import urllib, json
import urllib2

import syslog
import time
import sys
import random
import threading
import re
import shaney

from subprocess import call

def get_status():
  try:
    f = open('/tmp/status', 'r')
    s = f.read(1)
    f.close()
    return s
  except:
    return "0"

def update_status():
  f = open('/tmp/status', 'w')
  f.write("0")
  f.close()

def get_txt():
  try:
    f = open('/tmp/data', 'r')
    return f.read()
  except:
    return 'Sorry. No data.' 

def get_last():
  try:
    f = open('/tmp/last', 'r')
    return f.read()
  except:
    return 'Sorry. No data.' 

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        #self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        txt = ''
        clazz = ''

        if get_status() == "1":
          txt = get_last()
          clazz = 'new'
          update_status()
        else:
          txt = get_txt()
          txt = shaney.do_shaney(txt)

        if self.path == '/':
          self.path = '/index.html'


        try:
       	  f = open('./' + self.path)
          template = f.read() 
          res = template.replace('THE_TEXT', txt)
          res = res.replace('THE_CLASS', clazz)
          self.wfile.write(res)
          f.close()
          return
        except IOError:
          self.send_error(404, 'file not found')

    def do_HEAD(self):
        self._set_headers()

def run_server(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    #httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./77867815_localhost.pem', server_side=True)
    print 'Starting httpd... (http://localhost:%s/)' % port
    httpd.serve_forever()

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=80)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    run_server(port=args.port)

