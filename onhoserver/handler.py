#!/usr/bin/env python
#-*- coding: utf-8 -*-
from onhocommon import version
import simplejson as json

def handle(socket, address):
    print ('+New connection from %s:%s' % address)
    # using a makefile because we want to use readline()
    fileobj = socket.makefile()
    fileobj.write('Welcome to the ONHO server!.\r\n')
    fileobj.write('Version: ' + version.SERVER_VERSION + ' (rev' + version.REV + ')\r\n')
    fileobj.flush()
    while True:
        line = fileobj.readline()
        if not line:
            print ("-client disconnected"), address
            break
        if line.strip().lower() == 'quit':
            print ("-client quit"), address
            break
        try:
            python_object = json.loads(line)
            print 'Odebrano JSON:'
            print python_object
            for key in python_object.keys():
                print key, '=', python_object[key]
        finally:
            pass
        fileobj.write(line)
        fileobj.flush()
        print ("echoed %r" % line)

#test = (1, 2, 3, 4, 5)
#print test
#    json_object = json.dumps(test)
#    print json_object
#python_object = json.loads(json_object)

if __name__ == '__main__':
    import main
