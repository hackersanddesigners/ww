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

count = 1

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
      global count
      self._set_headers()
      txt = ''
      clazz = ''
      res = ''
      inc = False

      try:
        if self.path == '/' or "index" in self.path:
          inc = True
          self.path = '/index.html'
        f = open('./' + self.path)
        template = f.read() 
        f.close()

        if get_status() == "1":
          txt = get_last()
          print "TXT" + txt
          clazz = 'new'
          update_status()
          res = template.replace('THE_TEXT1', txt)
          res = res.replace('THE_CLASS', clazz)
          res = res.replace('THE_COUNT1', str(count))
          if inc: 
            count = count + 1
          for i in range(2, 5):
            res = res.replace('THE_TEXT'+str(i), "")
            res = res.replace('THE_COUNT'+str(i), "")
        else:
          txt = get_txt()
          res = template.replace('THE_CLASS', "")
          for i in range(1, 5):
            stxt = shaney.do_shaney(txt)
            res = res.replace('THE_TEXT'+str(i), stxt)
            res = res.replace('THE_COUNT'+str(i), str(count))
            if inc: 
              count = count + 1
        self.wfile.write(res)
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

