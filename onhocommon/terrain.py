#!/usr/bin/python
#-*- coding: utf-8 -*-

class TerrainType(object):
    '''Class defining terrain types which can additionally describe board hex'''
    NONE = 0
    THICK = 1
    HIGH = 2
    DISMAL = 3
    POISONOUS = 4
    JUNGLE = 5
    ROCKY = 6
    FORTRESS = 7
    WATCHTOWER = 8
    DEEP = 9
    WHIRLLPOOL = 10
    SWAMP = 11
    PLAIN = 12
    RADIOACTIVE = 13
    CLOSED = 14
    DEFENSE_SYSTEM = 15
    TURRET = 16
    CONTROL_PANEL = 17
    TIGHT = 18
    PRIZE = 19
    FATAL = 20

class TerrainTile(object):
    '''Class defining how board hex can look like on map'''
    NONE = 0
    FOREST = 1
    HILL = 2
    WATER = 3
    WASTELAND = 4
    ROCK = 5
    HOLE = 6
