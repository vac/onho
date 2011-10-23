#!/usr/bin/python
#-*- coding: utf-8 -*-

class Armies:
    UNKNOWN = 0
    MOLOCH = 1
    BORGO = 2
    OUTPOST = 3
    HEGEMONY = 4
    NEW_YORK = 5
    NEOJUNGLE = 6
    SMART = 7
    VEGAS = 8

class test(object):
    def __init__(self):
        self.i = 1
    def add(self):
        self.i += 1;
    def copy(self):
        return copy.deepcopy(self)

a = test()
a.add();
#print a
b = test()
b.add()
b.add()
import copy
lista = [[a.copy()] * 2 + [b] * 3]
#print zip(lista)

t = ['a'] * 5 + ['b']
print t

