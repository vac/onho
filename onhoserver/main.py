#!/usr/bin/env python
#-*- coding: utf-8 -*-
from gevent.server import StreamServer
import sys, getopt
from handler import handle
from onhocommon import version

def usage():
    print '''
    --help
    --port=7872
    --ip=0.0.0.0
    '''


port = 7872
ip = '0.0.0.0'
try:
    opts, args = getopt.getopt(sys.argv, "hp:d", ["help", "port=", "ip="])
except getopt.GetoptError:
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    if opt == "--ip":
        ip = arg
    elif opt == '-d':
        global _debug
        _debug = 1
    elif opt in ("-p", "--port"):
        port = arg

server = StreamServer((ip, port), handle)

print u'ONHO Server'
print u'Version:', version.SERVER_VERSION, u'(rev' + str(version.REV) + ')'
print u'Build date:', version.BUILD_DATE, version.BUILD_TIME
print u'----------------------------'
print u'Listening on', ip, ':', port
server.serve_forever()

