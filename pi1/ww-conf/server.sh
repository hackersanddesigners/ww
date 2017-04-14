#! /usr/bin/env python
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
import bot

from subprocess import call, Popen

print_content = ''
status = "0"

def check_status():
		try:
			file = open("/tmp/status", "r")
			s = file.read(1)
			file.close()
			return s
		except:
			return "0"

def end_session():
    global print_content
    print_content =''
    try:
        call(["umount", "/mnt"])
    except:
        print "Nothing to umount."
    file = open("/tmp/status", "w")
    file.write("0")
    file.close()

def create_content(str, img):
    content = str
    global print_content
    print_content = print_content + content

def get_imgur(transcript):
    types = ['png', 'jpg', 'gif', 'anigif']
    rtype = types[random.randint(0, len(types) - 1)]
    words = transcript.split()
    words = sorted(words, key=len)
    word = words[len(words) - 1]
    url = 'https://api.imgur.com/3/gallery/search?q=' + urllib.quote(word) +'&q_type=' + rtype
    req = urllib2.Request(url)
    req.add_header('Authorization', 'Client-ID 62a1dd4dde196de')
    resp = urllib2.urlopen(req)
    data = json.loads(resp.read())
    urls = []
    for item in data['data']:
        try:
            url = item['link']
            if url.startswith('http'):
                urls.append(url)
        except:
            pass

    if urls:
        n = random.randint(0, len(urls) - 1)
        print 'found image: %s' % urls[n]
        return urls[n]
    else:
        print 'found no image'
        return ' '

def get_image(transcript):
    url = 'https://www.googleapis.com/customsearch/v1?q=' + urllib.quote(transcript) + '&safe=off&num=10&cx=015700006039354317064:q1iz_ozoiqg&key=AIzaSyA4uO6dS4qA3D6NxfzaIXPQsWir8L_nT1A&alt=json'
    resp = urllib.urlopen(url)
    data = json.loads(resp.read())
    urls = []

    for item in data['items']:
        try:
            url = item['pagemap']['cse_image'][0]['src']
            if url.startswith('http'):
                urls.append(url)
        except:
            pass

    if urls:
        n = random.randint(0, len(urls) - 1)
        print 'found image: %s' % urls[n]
        return urls[n]
    else:
        print 'found no image'
        return ' '


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

    def do_POST(self):
        # Extract and print the contents of the POST
        length = int(self.headers['Content-Length'])
        post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
        transcript = None
        for key, values in post_data.iteritems():
            for value in values:
                print 'post %s %r' % (key, value)
                if key == 'str':
                    transcript = value

        self._set_headers()
        if transcript:
            #url = get_imgur(transcript)
            url = ''
            create_content(transcript, url)
            q = "Your session has ended. Please remove your USB."
            status = check_status()
            global print_content
            print("COUNT: " + str(len(print_content)) + " STATUS: " + str(status))
            f = open("/mnt/data", "a")
            f.write(transcript + ". ")
            f.close()
            if len(print_content) < 350 and status != "0":
                q = bot.analyze(transcript)
            else:
                end_session()
            self.wfile.write(json.dumps({'i': url, 'q': q, 's': status}))
            Popen(["espeak", q])
        else:
            self.wfile.write('Failed image search.')

def run_server(server_class=HTTPServer, handler_class=S, port=443):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./77867815_localhost.pem', server_side=True)
    print 'Starting httpd... (https://localhost:%s/)' % port
    httpd.serve_forever()

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=443)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    run_server(port=args.port)

