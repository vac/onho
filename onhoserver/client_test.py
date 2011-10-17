#!/usr/bin/env python
#-*- coding: utf-8 -*-
import socket
import simplejson as json
import time
HOST = '127.0.0.1'
PORT = 7872
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

test_dict = dict(move=(10, 1), bumbum=['Borgo', '''Hegemonia
1'''])
json_object = json.dumps(test_dict)
s.send(json_object)
data = s.recv(1024)

time.sleep(1)

test_dict = dict(move=(20, 2.1475), bumbum=['Borgo2', '''Hegemonia
2'''])
json_object = json.dumps(test_dict)
s.send(json_object)
data = s.recv(1024)
s.close()
print 'Received', repr(data)
