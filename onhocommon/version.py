#!/usr/bin/python
#-*- coding: utf-8 -*-
'''ONHO current versions'''

import re
from datetime import date
import time

VERSION = '0'
CLIENT_VERSION = '0'
SERVER_VERSION = '0'

BUILD_DATE = date.today()
BUILD_TIME = time.strftime('%H:%M')

def get_svn_revision(path=None):
    """
    Contributed from Django (https://code.djangoproject.com/browser/django/trunk/django/utils/version.py)
    
    Returns the SVN revision in the form SVN-XXXX,
    where XXXX is the revision number.

    Returns SVN-unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.

    If path is provided, it should be a directory whose SVN info you want to
    inspect. If it's not provided, this will use the root parent directory.
    """
    rev = 0
    if path is None:
        path = '..'
    entries_path = '%s/.svn/entries' % path

    try:
        entries = open(entries_path, 'r').read()
    except IOError:
        pass
    else:
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if re.match('(\d+)', entries):
            rev_match = re.search('\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
        # Older XML versions of the file specify revision as an attribute of
        # the first entries node.
        else:
            from xml.dom import minidom
            dom = minidom.parse(entries_path)
            rev = dom.getElementsByTagName('entry')[0].getAttribute('revision')

    return rev

CLIENT_REV = 0
SERVER_REV = 0
REV = get_svn_revision()

if __name__ == '__main__':
    print 'Revision:', REV
    print 'Date:', BUILD_DATE
    print 'Time:', BUILD_TIME