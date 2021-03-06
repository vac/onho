#!/usr/bin/env python
#-*- coding: utf-8 -*-
from orientation import all_directions
from onhocommon.orientation import all_directions

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
    def __init__(self,
                initiative=[0],
                mobility=0,
                toughness=0,
                bomb=0,
                poisonous=0,
                spy=0,
                push=0,
                transport=0,
                sniper=0,
                pile=0,
                net=all_directions(0),
                armor=all_directions(0),
                attack_melee=all_directions(0),
                attack_ranged=all_directions(0),
                attack_gauss=all_directions(0),
                attack_homing=all_directions(0),
                attack_narrow=all_directions(0),
                 ** kwargs):
        super(Unit, self).__init__(**kwargs)
        self.type_id = Type.UNIT

        self.initiative = [] + initiative
        self.mobility = mobility
        self.toughness = toughness
        self.bomb = bomb #Clown
        self.poisonous = poisonous
        self.spy = spy
        self.push = push #pusher
        self.transport = transport #transporter
        self.sniper = sniper
        self.pile = pile #bio-droid
        self.net = net
        self.armor = armor
        self.attack_melee = attack_melee
        self.attack_ranged = attack_ranged
        self.attack_gauss = attack_gauss
        self.attack_homing = attack_homing #bazooka
        self.attack_narrow = attack_narrow #shotgun

class Module(Board):
    '''Class representing all modules tiles'''
    def __init__(self,
                mobility=0,
                toughness=0,
                armor=all_directions(0),
                takeover=all_directions(0),
                heal=all_directions(0),
                bonus_initiative=all_directions(0),
                bonus_toughness=all_directions(0),
                bonus_mobility=all_directions(0),
                bonus_attack_melee=all_directions(0),
                bonus_attack_ranged=all_directions(0),
                bonus_action=all_directions(0),
                bonus_abbility=all_directions(0),
                bonus_filter=None,
                special_filter=None,
                special_decorator=None,
                 ** kwargs):
        super(Module, self).__init__(**kwargs)
        self.type_id = Type.MODULE

        self.mobility = mobility
        self.toughness = toughness

        self.armor = armor

        self.takeover = takeover #agitator
        self.heal = heal #medic

        self.bonus_initiative = bonus_initiative #scout +1, saboteur -1
        self.bonus_toughness = bonus_toughness #NY HQ
        self.bonus_mobility = bonus_mobility #transport
        self.bonus_attack_melee = bonus_attack_melee #officer I
        self.bonus_attack_ranged = bonus_attack_ranged #officer II
        self.bonus_action = bonus_action #mother

        self.bonus_abbility = bonus_abbility #quartermaster
        self.bonus_filter = bonus_filter #Scoper - jakie rodzje jednostek beda podelgały działaniu modułu

        self.special_filter = special_filter #recon center, quartermaster
        self.special_decorator = special_decorator #recon center, quartermaster


class HeadQuarter(Module):
    '''Class representing all headquarters tiles'''
    def __init__(self,
                 initiative=[0],
                 attack_melee=all_directions(1),
                 ** kwargs):
        super(HeadQuarter, self).__init__(**kwargs)
        self.type_id = Type.HEADQUARTER
        self.initiative = [] + initiative
        self.attack_melee = attack_melee

class Foundation(Board):
    '''Class representing all foundation/terrain tiles'''
    def __init__(self, **kwargs):
        super(Foundation, self).__init__(**kwargs)
        self.type_id = Type.FOUNDATION
        self.foundation = kwargs.get('foundation', Foundations.NONE)
