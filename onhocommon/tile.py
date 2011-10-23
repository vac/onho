#!/usr/bin/env python
#-*- coding: utf-8 -*-
from orientation import all_directions

class Type:
    UNKNOWN = 0
    ACTION = 1
    BOARD = 2
    UNIT = 3
    MODULE = 4
    HEADQUARTER = 5
    FOUNDATION = 6

class Actions:
    NONE = 0
    UNKNOWN = 0
    BATTLE = 1
    MOVE = 2
    PUSH = 3
    SNIPER = 4
    CASTLING = 5
    ROTATION = 6
    GRANADE = 7
    BOMB = 8
    SMALL_BOMB = 9
    TERROR = 10

class Abbilities:
    NONE = 0
    UNKNOWN = 0
    ONE_ATTACK_SWAP = 1 #quatermaster 

class Foundations:
    UNKNOWN = 0
    NONE = 0
    MINE = 1
    ROOTS = 2 #Jungle

class Tile(object):
    def __init__(self, **kwargs):
        self.type_id = Type.UNKNOWN
        for key in kwargs:
            print key

class Action(Tile):
    '''Class representing all instant action tiles'''
    def __init__(self, **kwargs):
        super(Action, self).__init__(**kwargs)
        self.type_id = Type.ACTION
        self.action = kwargs.get('action', Actions.NONE)

class Board(Tile):
    '''Class representing all tiles that can be places on board'''
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.type_id = Type.BOARD

class Unit(Board):
    '''Class representing all units/soldiers tiles'''
    def __init__(self, **kwargs):
        super(Unit, self).__init__(**kwargs)
        self.type_id = Type.UNIT

        self.initiative = [0]
        self.mobility = 0
        self.toughness = 0
        self.poisonous = 0
        self.spy = 0
        self.push = 0 #pusher
        self.transport = 0 #transporter
        self.sniper = 0
        self.pile = 0 #bio-droid
        self.net = all_directions(0)
        self.attack_melee = all_directions(0)
        self.attack_ranged = all_directions(0)
        self.attack_gauss = all_directions(0)
        self.attack_homing = all_directions(0) #bazooka
        self.attack_narrow = all_directions(0) #shotgun
        self.armor = all_directions(0)

class Module(Board):
    '''Class representing all modules tiles'''
    def __init__(self, **kwargs):
        super(Module, self).__init__(**kwargs)
        self.type_id = Type.MODULE

        self.mobility = 0
        self.toughness = 0

        self.armor = all_directions(0)

        self.takeover = all_directions(0) #agitator
        self.heal = all_directions(0) #medic

        self.bonus_initiative = all_directions(0) #scout +1, saboteur -1
        self.bonus_toughness = all_directions(0) #NY HQ
        self.bonus_mobility = all_directions(0) #transport
        self.bonus_attack_melee = all_directions(0) #officer I
        self.bonus_attack_ranged = all_directions(0) #officer II
        self.bonus_action = all_directions(0) #mother

        self.bonus_abbility = all_directions(0) #quartermaster
        self.bonus_filter = None #Scoper - jakie rodzje jednostek beda podelgały standardowym bonusom

        self.special_filter = None #recon center, quartermaster
        self.special_decorator = None #recon center, quartermaster


class HeadQuarter(Module):
    '''Class representing all headquarters tiles'''
    def __init__(self, **kwargs):
        super(HeadQuarter, self).__init__(**kwargs)
        self.type_id = Type.HEADQUARTER
        self.initiative = [0]
        self.attack_melee = all_directions(1)

class Foundation(Board):
    '''Class representing all foundation/terrain tiles'''
    def __init__(self, **kwargs):
        super(Foundation, self).__init__(**kwargs)
        self.type_id = Type.FOUNDATION
        self.foundation = kwargs.get('foundation', Foundations.NONE)
