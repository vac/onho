#!/usr/bin/python
#-*- coding: utf-8 -*-
import Image, ImageDraw
from ImageDraw import Draw
from math import sqrt, ceil, floor
from itertools import izip
import maps
import unittest

class BoardHex(object):
    '''Class defining all possible hex on board'''
    NONE = 0
    NORMAL = 1
    TERMINAL = 2

class Board(object):
    def __init__(self, *args, **kwargs):
        self.map = kwargs.get('map', maps.STANDARD)
        self.width = kwargs.get('width', 640)
        self.height = kwargs.get('height', 480)
        self.hex_margin = kwargs.get('hex_margin', 20)
        self.board_margin = kwargs.get('board_margin', 0)

    def hex_size(self):
        a = self.hex_a()
        return 2 * a, a * sqrt(3)

    def hex_a(self):
        if self.width <= 0 or self.height <= 0:
            return 0
        if self.width <= self.board_margin or self.height <= self.board_margin:
            return 0

        size = self.map_size()
        if size == (0, 0):
            return 0

        a_from_width = (self.width - 2 * self.board_margin - (size[0] - 1) * self.hex_margin - 1) / (size[0] * 1.5 + 1 / 2.0)
        a_from_height = (self.height - 2 * self.board_margin - 1 - (size[1] - 1) * self.hex_margin * sqrt(3) / 2.0) / (size[1]*sqrt(3))

        return min(a_from_width, a_from_height)

    def all_indexes(self):
        """Zwraca wszystkie możliwe indeksy pól na mapie"""
        for col in range(11):
            for row in range(7):
                if not((col % 2 == 0) and (row == 6)):
                    yield (col, row)

    def map_indexes(self):
        '''Zwraca indeksy pól na mapie'''
        if self.map:
            if len(self.map) > 0:
                if len(self.map[0]) > 0:
                    return (m[0] for m in self.map)
        return None

    def map_cols(self):
        '''zwraca wszystkei kolumny na mapie'''
        if self.map:
            if len(self.map) > 0:
                if len(self.map[0]) > 0:
                    return list(set((index[0] for index in self.map_indexes())))
        return None

    def map_col(self, col):
        '''zwraca wiersze wskazanej kolumny mapy'''
        for index in self.map_indexes():
            if index[0] == col:
                yield index[1]

    def map_row(self, row):
        '''zwraca kolumny wskazanego wiersza mapy'''
        for index in self.map_indexes():
            if index[1] == row:
                yield index[0]

    def map_rows(self):
        '''zwraca indeksy wierszy na mapie'''
        return list(set((index[1] for index in self.map_indexes())))

    def map_width(self):
        '''zwraca szerokosc mapy jako liczbe pól'''
        x = self.map_cols()
        if x:
            return max(x) - min(x) + 1
        else:
            return 0

    def _get_lower_columns(self):
        if self.map:
            if len(self.map[0]) > 0:
                for col in self.map_cols():
                    if col % 2 == 0:
                        yield col

    def _get_higher_columns(self):
        if self.map:
            if len(self.map[0]) > 0:
                for col in self.map_cols():
                    if col % 2 == 1:
                        yield col

    def map_height(self):
        '''Zwraca wysokosc mapy w liczbie pól. Połówka oznacza, że jest różnica pół hexa pomiędzy kolumnami.'''
        lower = None
        higher = None
        if sum(1 for j in self._get_lower_columns()) > 0:
            lower = (
                #minimalny wiersz w kolumnach "nizszych"
                min(min(self.map_col(col)) for col in self._get_lower_columns()),
                #maksymalny wiersz w kolumnach "nizszych"
                max(max(self.map_col(col)) for col in self._get_lower_columns())
            )
        if sum(1 for j in self._get_higher_columns()) > 0:
            higher = (
                #minimalny wiersz w kolumnach "wyzszych"
                min(min(self.map_col(col)) for col in self._get_higher_columns()) - 0.5,
                #maksymalny wiersz w kolumnach "wyzszych"
                max(max(self.map_col(col)) for col in self._get_higher_columns()) - 0.5
            )
        if higher and lower:
            return max(higher[1], lower[1]) - min(higher[0], lower[0]) + 1
        if higher:
            return higher[1] - higher[0] + 1
        if lower:
            return lower[1] - lower[0] + 1
        return 0

    def map_size(self):
        return self.map_width(), self.map_height()


def field_center(hex_a=68, margin_x=20, offset_x=None, offset_y=None):
    """Zwraca srodki pól na mapie w px"""
    margin_y = margin_x * sqrt(3) / 2.0
    if not offset_x:
        offset_x = hex_a
    if not offset_y:
        offset_y = hex_a * sqrt(3) + margin_y / 2
    for col, row in board_indexes():
        yield (
            offset_x + col * margin_x + col * 1.5 * hex_a,
            offset_y + row * margin_y + row * hex_a * sqrt(3) - (col % 2) * (hex_a * sqrt(3) / 2.0 + margin_y / 2)
        )

def fld(hex_a, margin_x, indeksy, kolumny, wiersze):
    margin_y = margin_x * sqrt(3) / 2.0
    offset_x = hex_a
    offset_y = hex_a * sqrt(3) + margin_y / 2
    col_offset = min(kolumny)
    row_offset = min(wiersze)
    for col, row in indeksy:
        yield (
            offset_x + (col - col_offset) * margin_x + (col - col_offset) * 1.5 * hex_a,
            offset_y + (row - row_offset) * margin_y + (row - row_offset) * hex_a * sqrt(3) - (col % 2) * (hex_a * sqrt(3) / 2.0 + margin_y / 2)
        )

def board_cols():
    return list(set((index[1] for index in board_indexes())))

def board_rows():
    return list(set((index[0] for index in board_indexes())))

def board_size_px(hex_a=68, margin_x=20):
    izip(*board_indexes())

def board_indexes():
    """Zwraca indeksy pól na mapie"""
    for col in range(11):
        for row in range(7):
            if not((col % 2 == 0) and (row == 6)):
                yield (col, row)
#max_x = 0
#min_x = 1000
#max_y = 0
#min_y = 1000
def draw_hex(srodek, a):
    return (
        srodek[0] - a, srodek[1],
        int(srodek[0] - a / 2.0), int(srodek[1] + a * sqrt(3) / 2.0),
        int(srodek[0] + a / 2.0), int(srodek[1] + a * sqrt(3) / 2.0),
        srodek[0] + a, srodek[1],
        int(srodek[0] + a / 2.0), int(srodek[1] - a * sqrt(3) / 2.0),
        int(srodek[0] - a / 2.0), int(srodek[1] - a * sqrt(3) / 2.0)
    )
plansza = Board(map=maps.TEST)
plansza.width = 640
plansza.height = 640

im = Image.new('RGBA', (
                       plansza.width,
                       plansza.height
                       ))
draw = ImageDraw.Draw(im)
#index = board_indexes()
#plansza = Board(map=maps.TEST)
for srodek in fld(plansza.hex_a(), plansza.hex_margin, plansza.map_indexes(), plansza.map_cols(), plansza.map_rows()):
    draw.polygon(draw_hex(srodek, plansza.hex_a()), outline='#0000FF')
#    draw.text(srodek, str(index.next()), fill='#000000')
#    #draw.text((srodek[0] + 20, srodek[1] + 20), str(index[0]) + ',' + str(index[1]), fill=128)
del Draw
im.save('board.png', "PNG")

class TestBoardFunctions(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_map_size(self):
        self.board.map = (),
        self.assertEqual(self.board.map_size(), (0, 0))

        self.board.map = (((3 , 2),),)
        self.assertEqual(self.board.map_size(), (1, 1))

        self.board.map = (((0 , 0),),)
        self.assertEqual(self.board.map_size(), (1, 1))

        self.board.map = (((0 , 0),), ((2, 0),))
        self.assertEqual(self.board.map_size(), (3, 1))

        self.board.map = (((0 , 0),), ((0, 5),))
        self.assertEqual(self.board.map_size(), (1, 6))

        self.board.map = (((0 , 0),), ((1, 1),))
        self.assertEqual(self.board.map_size(), (2, 1.5))

        self.board.map = (((0 , 0),), ((10, 5),), ((9, 6),))
        self.assertEqual(self.board.map_size(), (11, 6.5))

if __name__ == '__main__':
    unittest.main()
