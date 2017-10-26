#!/usr/bin/python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import json
import SocketServer
import ssl 
import syslog
#import time
import sys
import select
#import random
import threading
#import re
import shaney 
import os

clients = []
count = 1

def get_status():
  try:
    f = open('/data/status', 'r')
    s = f.read(1)
    f.close()
    return s
  except:
    return "0"

def update_status():
  f = open('/data/status', 'w')
  f.write("0")
  f.close()

def get_txt():
  try:
    f = open('/data/data', 'r')
    return f.read()
  except:
    return 'Sorry. No data.' 

def get_last():
  try:
    f = open('/data/last', 'r')
    return f.read()
  except:
    return 'Sorry. No data.' 

def write_txt(c, txt):
  txt = str(c)+"\t"+txt+"\n"
  print txt
  with open("/data/scripture", "a") as f:
    f.write(txt)

class WSClient(WebSocket):
  def handleMessage(self):
    return

  def handleConnected(self):
    #print self.address, 'connected'
    clients.append(self)

  def handleClose(self):
    #print self.address, 'closed'
    clients.remove(self)

class S(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    #self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self._set_headers()
    if self.path == '/':
      self.path = '/index.html'
    f = open('./' + self.path)
    try:
      self.wfile.write(f.read())
      f.close()
      return
    except IOError:
      self.send_error(404, 'file not found')

  def do_HEAD(self):
    self._set_headers()

def broadcast(count, txt, note):
  resp = {
    'count': count,
    'txt': txt,
    'note': note 
  }
  json_str = json.dumps(resp)
  global clients
  for client in clients:
    client.sendMessage(json_str)

def note_loop():
  while True:
    if get_status() == "1":
      txt = get_last()
      broadcast(count, txt, true)
      update_status()
      write_txt(count, txt)
      count = count + 1
    thread.sleep(0.1)

def loop():
  while True:
    if get_status() == "0":
      txt = get_txt()
      shaney.do_shaney(txt)
      broadcast(count, txt, false)
      write_txt(count, txt)
      count = count + 1
    thread.sleep(10)

def run_server(server_class=HTTPServer, handler_class=S, port=443):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  #httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./77867815_localhost.pem', server_side=True)
  print 'Starting httpd... (https://localhost:%s/)' % port
  httpd.serve_forever()

note_thread = threading.Thread(target=note_loop)
note_thread.daemon = True
note_thread.start()

thread = threading.Thread(target=loop)
thread.daemon = True
thread.start()

http_thread = threading.Thread(target=run_server)
http_thread.daemon = True
http_thread.start()

server = SimpleWebSocketServer('', 8000, WSClient)
server.serveforever()

