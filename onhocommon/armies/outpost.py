#!/usr/bin/python
#-*- coding: utf-8 -*-
from onhocommon.tile import Unit, Module, HeadQuarter
from onhocommon.orientation import directed, all_directions, around

'''
Kierunki świata:

       N
    /-----\
NW /       \ NE
  /         \
  \         /
SW \       / SE
    \-----/
       S

możliwości kierunkowe:
directed(N=liczba, ....)
np:
directed(N=1, NE=2)
directed(S=1)
directed(NE=1, SE=1, SW=1, NW=1)

a jak chcemy we wszystkich kierunkach to skrót jest:
all_directions(1) lub around(1) odpowiada temu samemu co directed(N=1, NE=1, SE=1, S=1, SW=1, NW=1)

Możliwości jednostek (Unit):

tablice:
initiative

wartość liczbowa: 
mobility 
toughness 
bomb 
poisonous 
spy
push 
transport
sniper 
pile 

Kierunkowe (te z directed):
net 
armor 
attack_melee 
attack_ranged 
attack_gauss 
attack_homing 
attack_narrow 


Możliwości modułów (Module):

Liczbowe:
mobility
toughness

Kierunkowe:
armor
takeover
heal
bonus_initiative 
bonus_toughness 
bonus_mobility 
bonus_attack_melee 
bonus_attack_ranged
bonus_action

Wyjątkowe:
bonus_abbility
bonus_filter
special_filter 
special_decorator
'''

HQ = HeadQuarter(bonus_action=around(1))

Runner = Unit(
              initiative=[2],
              mobility=1,
              attack_melee=directed(N=1)
)

HMG = Unit(
    initiative=[2, 1],
    attack_ranged=directed(N=1)
)

Commando = Unit(initiative=[3], attack_ranged=directed(N=1))

Annihilator = Unit(
                initiative=[2],
                attack_ranged=directed(N=1))

Mobile_Armor = Unit(
                initiative=[3, 2],
                mobility=1,
                attack_melee=directed(N=2),
                attack_ranged=directed(NW=1)
)

#Brawler

Saboteur = Module(bonus_initiative=around(-1))

Medic = Module(heal=directed(N=1, NW=1, NE=1))

#TODO wypełnić brakujące jednostki


#poniżej dwa elemety, które nie do końca jeszcze logicznie się opisuje:
Scoper = Module(takeover=around(1), bonus_filter=(1)) #TODO jakiś logiczny bonus filter tylko dla wrogich modułów

Recon_Center = Module(
                      special_decorator=('mobility', '+1'), #TODO sensownie rozwiązać special_decorator
                      special_filter=('moje jednostki z mobility>0') #TODO sensownie rozwiązać special_filter
)
