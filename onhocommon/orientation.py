#!/usr/bin/env python
#-*- coding: utf-8 -*-
from numpy import array
import unittest

class Direction:
    '''Klasa definiująca indeksy kierunków'''
    N = 0 #North
    NE = 1 #North East
    SE = 2 #South East
    S = 3 #South
    SW = 4 #South West
    NW = 5 #North West

'''Wszystkie kierunki w początkowym ustawieniu'''
Directions = array([Direction.N, Direction.NE,
                    Direction.SE, Direction.S,
                    Direction.SW, Direction.NW
            ])

def all_directions(value):
    return array([value] * 6)

def around(value):
    return all_directions(value)

def directed(N=0, NE=0, SE=0, S=0, SW=0, NW=0):
    return array([N, NE, SE, S, SW, NW])

class Position(object):
    INDEX = 0 #index of position index in tuple
    ROTATION = 1 #index of rotation in tuple

    def __init__(self, index, rotation=0, *args, **kwargs):
        self.index = array([index[0], index[1]])
        #jezeli obrot jest wiekszy lub rowny 60 tzn ze zostal podany w stopniach
        if rotation >= 60:
            rotation = rotation / 60

        #gdyby obrót nie był o pełną wielokrotnośc to w razie czego zaokrąglamy
        self.rotation = int(round(rotation % 6))

    @property
    def rotation_deg(self):
        '''Zwraca obrót w stopniach'''
        return self.rotation * 60

    def rotate_right(self, times=1):
        '''Rotate tile right number of times'''
        self.rotate(times)

    def rotate_left(self, times=1):
        '''Rotate tile left number of times'''
        self.rotate(-times)

    def rotate_deg(self, deg):
        '''Rotate tile by specified amount of degree'''
        self.rotate((deg / 60) % 6)

    def rotate(self, rotation_times):
        '''Rotate tile specified times. 
        Negative number -> rotate left. 
        Positive number -> rotate right.'''
        self.rotation_set((self.rotation + rotation_times) % 6)

    def rotation_set(self, rotation):
        '''Sets the absolute rotation'''
        if rotation >= 60:
            rotation = rotation / 60
        self.rotation = int(round(rotation % 6))

    @property
    def as_tuple(self):
        return (self.x, self.y, self.rotation)
    @as_tuple.setter
    def as_tuple(self, value):
        if value.get(Position.X) != None:
            self.x = value[Position.X]
        if value.get(Position.Y) != None:
            self.y = value[Position.Y]
        if value.get(Position.Z) != None:
            self.rotation_set(value[Position.ROTATION])

    @property
    def as_dict(self):
        return dict(x=self.index[0], y=self.index[1], index=self.index, rotation=self.rotation)

    @as_dict.setter
    def as_dict(self, value):
        if value.get('x') != None:
            self.index[0] = value['x']
        if value.get('y') != None:
            self.index[1] = value['y']
        if value.get('index') != None:
            self.index[0] = value['index'][0]
            self.index[1] = value['index'][1]
        if value.get('rotation') != None:
            self.rotation_set(value['rotation'])

    @property
    def as_array(self):
        return array([self.index[0], self.index[1], self.rotation])
    @as_array.setter
    def as_array(self, value):
        if len(value) > Position.X:
            self.index[0] = value[Position.X]
        if len(value) > Position.Y:
            self.index[1] = value[Position.Y]
        if len(value) > Position.ROTATION:
            self.rotation_set(value[Position.ROTATION])

    def move_vectors(self):
        '''Zwraca wektory ruchu w każdym z kierunków dla danej pozycji żetonu'''
        return array([
                [0, -1], #N
                [1, -(self.index[0] % 2)], #NE
                [1, (self.index[0] + 1) % 2], #SE
                [0, 1], #S
                [-1, (self.index[0] + 1) % 2], #SW
                [-1, -(self.index[0] % 2)] #NW
        ])

    def move_vector(self, direction):
        '''Zwraca vector o jaki powinna ruszyć się jednostka gdy chce pójść w danym kierunku'''
        return self.move_vectors()[direction % 6]

    def directions(self):
        '''Zwraca indexy kierunków danego żetonu już po obrocie'''
        return (Directions - self.rotation) % 6


class TestOrientationFunctions(unittest.TestCase):
    def test_vectors(self):
        for x in range(11):
            for y in range(7):
                self.assertEqual(Position((x, y), 0).move_vector(Direction.N)[0], 0)
                self.assertEqual(Position((x, y), 0).move_vector(Direction.N)[1], -1)

                self.assertEqual(Position((x, y), 0).move_vector(Direction.S)[0], 0)
                self.assertEqual(Position((x, y), 0).move_vector(Direction.S)[1], 1)
    def test_rotation_directions(self):
        for rot in range(6):
            self.assertEqual(Position((0, 0), rot).directions()[rot], 0)


if __name__ == '__main__':
    #unittest.main()
    value = 0
