#!/usr/bin/python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from subprocess import call, Popen
from pynput import keyboard

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
import bot
import os

start_txt = "Please insert a USB and press start."

clients = []

def startSession():
  if hasUSB():
    f = open(getFilename(), 'w')
    f.write('');
    f.close()
  else:
    broadcast(start_txt)

def writeContent(transcript):
  f = open(getFilename(), 'a')
  f.write(transcript + '. ')
  f.close()

def endSession():
  Popen(['osascript', '-e', 'tell application "Finder" to eject (every disk whose ejectable is true)'])

def hasUSB():
  l = os.listdir('/Volumes')
  l.remove('Macintosh HD')
  l.remove('.DS_Store')
  return len(l) > 0

def getFilename():
  l = os.listdir('/Volumes')
  l.remove('Macintosh HD')
  l.remove('.DS_Store')
  return '/Volumes/' + l[0] + '/data'

class WSClient(WebSocket):
  def handleMessage(self):
    # echo message back to client
    #self.sendMessage(self.data)
    if hasUSB(): 
      transcript = json.loads(self.data)['txt']
      writeContent(transcript)
      q = bot.analyze(transcript)
      broadcast(q)
    else:
      broadcast(start_txt)

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

def broadcast(txt):
  resp = {
    'txt': txt
  }
  json_str = json.dumps(resp)
  global clients
  for client in clients:
    client.sendMessage(json_str)
  Popen(["say", txt])

def on_press(key):
  return True 
#  try:
#    print('alphanumeric key {0} pressed'.format(
#      key.char))
#  except AttributeError:
#    print('special key {0} pressed'.format(
#      key))
#

def on_release(key):
  try:
    print('{0} released'.format(
      key))
    if key == keyboard.Key.esc:
      # Stop listener
      return False
    elif key.char == 'w':
      print('Start.')
      startSession()
    elif key.char == 's':
      print('End.')
      endSession()
  except AttributeError:
    return True

def loop():
  # Collect events until released
  with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
      listener.join()

def run_server(server_class=HTTPServer, handler_class=S, port=443):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./77867815_localhost.pem', server_side=True)
  print 'Starting httpd... (https://localhost:%s/)' % port
  httpd.serve_forever()

button_thread = threading.Thread(target=loop)
button_thread.daemon = True
button_thread.start()

http_thread = threading.Thread(target=run_server)
http_thread.daemon = True
http_thread.start()

server = SimpleWebSocketServer('', 8000, WSClient)
server.serveforever()

