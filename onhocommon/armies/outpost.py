#!/usr/bin/python
#-*- coding: utf-8 -*-
from onhocommon.tile import Unit, Module, HeadQuarter
from onhocommon.orientation import directed, all_directions, around

Runner = Unit(initiative=[2], mobility=1, attack_melee=directed(N=1))
