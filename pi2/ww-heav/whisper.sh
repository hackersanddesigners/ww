#!/usr/bin/env python

import time
import shaney
from subprocess import Popen
from random import randint

def get_txt():
  try:
    f = open('/data/data', 'r')
    return f.read()
  except:
    return 'Sorry. No data.' 

while True:
  txt = shaney.do_shaney(get_txt())
  p = randint(10, 100)
  s = randint(10, 100)
  v = "en+whisper" if randint(0, 1) == 0 else "en+whisperf"
  print v
  #Popen(["espeak", "-a", "10", "-p", str(p), "-s", str(s), "-v", v, txt])
  Popen(["espeak", "-a", "2", "-p", str(p), "-s", str(s), txt])
  time.sleep(randint(10,30))

