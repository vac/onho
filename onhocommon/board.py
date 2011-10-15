#!/usr/bin/python
#-*- coding: utf-8 -*-
from math import sqrt, ceil, floor
import maps
import unittest
import numpy as np


class BoardHex(object):
    '''Class defining all possible hex on board'''
    NONE = 0
    NORMAL = 1
    TERMINAL = 2

class Board(object):
    def __init__(self, *args, **kwargs):
        self.width, self.height = kwargs.get('size', (None, None))
        if not self.width:
            self.width = kwargs.get('width', 640)
        if not self.height:
            self.height = kwargs.get('height', 480)
        self.hex_margin = kwargs.get('hex_margin', 20)
        self.board_margin = kwargs.get('board_margin', 0)
        self._map = kwargs.get('map', maps.STANDARD)

        self._hex_size = None
        self._hex_a = None
        self._map_size = None
        self._map_indexes = None
        self._hex_centres = None
        self._min_col = None
        self._min_row = None

    def update(self):
        self._calc_map_indexes()
        if self.map_indexes != None:
            self._min_col = min(self.map_cols())
            self._min_row = min(self.map_rows())
        self._calc_map_size()
        self._calc_hex_a()

    @property
    def map(self):
        return self._map
    @map.setter
    def map(self, value):
        self._map = value
        self.update()

    @property
    def hex_size(self):
        return self._hex_size
    @hex_size.setter
    def hex_size(self, value):
        self._hex_size = value
        self._calc_hex_centres()

    def _calc_hex_size(self, a=None):
        if not a:
            a = self.hex_a
        self.hex_size = np.array([2 * a, a * sqrt(3)])

    @property
    def hex_a(self):
        '''Zwraca długość boku hexa'''
        return self._hex_a

    @hex_a.setter
    def hex_a(self, value):
        self._hex_a = value
        self._calc_hex_size()

    def _calc_hex_a(self):
        if self.width <= 0 or self.height <= 0:
            return 0
        if self.width <= self.board_margin or self.height <= self.board_margin:
            return 0

        size = self.map_size
        if size[0] == 0:
            return 0

        a_from_width = (
                        self.width - 2 * self.board_margin - (size[0] - 1) * self.hex_margin - 1
                        ) / (size[0] * 1.5 + 1 / 2.0)
        a_from_height = (self.height - 2 * self.board_margin - 1 - (size[1] - 1) * self.hex_margin * sqrt(3) / 2.0) / (size[1] * sqrt(3))

        self.hex_a = min(a_from_width, a_from_height)

    def all_indexes(self):
        """Zwraca wszystkie możliwe indeksy pól na mapie"""
        for col in range(11):
            for row in range(7):
                if not((col % 2 == 0) and (row == 6)):
                    yield (col, row)

    @property
    def map_indexes(self):
        '''Zwraca indeksy pól na mapie'''
        return self._map_indexes
    @map_indexes.setter
    def map_indexes(self, value):
        self._map_indexes = value

    def _calc_map_indexes(self):
        if self.map:
            if len(self.map) > 0:
                if len(self.map[0]) > 0:
                    self.map_indexes = np.array([m[0] for m in self.map])
                    return
        self.map_indexes = None

    def map_cols(self):
        '''Zwraca wszystkie kolumny na mapie'''
        if self.map_indexes != None:
            return list(set((index[0] for index in self.map_indexes)))
        return None

    def map_col(self, col):
        '''Zwraca wiersze wskazanej kolumny mapy'''
        for index in self.map_indexes:
            if index[0] == col:
                yield index[1]

    def map_row(self, row):
        '''Zwraca kolumny wskazanego wiersza mapy'''
        for index in self.map_indexes():
            if index[1] == row:
                yield index[0]

    def map_rows(self):
        '''zwraca indeksy wierszy na mapie'''
        return list(set((index[1] for index in self.map_indexes)))

    def _map_width(self):
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

    def _map_height(self):
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

    @property
    def map_size(self):
        return self._map_size

    @map_size.setter
    def map_size(self, value):
        self._map_size = value

    def _calc_map_size(self):
        width = self._map_width()
        height = self._map_height()
        self.map_size = np.array([width, height])

    def _approx_index(self, position):
        '''Zwraca w przyblizeniu index pola na podstawie pozycji w px'''
        col = self._min_col + (position[0] - self.hex_a) / (self.hex_margin + 1.5 * self.hex_a)
        row = self._min_row + (position[1] - self.hex_a * sqrt(3) - (self.hex_margin * sqrt(3) / 2.0) / 2.0 + (int(round(col)) % 2) * (self.hex_a * sqrt(3) / 2.0 + (self.hex_margin * sqrt(3) / 2.0) / 2.0)) / ((self.hex_margin * sqrt(3) / 2.0) + self.hex_a * sqrt(3))
        return (col, row)

    def _distances_to_hex(self, from_position):
        '''Zwraca odleglosci do wszystkich pol na mapie na podstawie pozycji w px'''
        return np.sqrt(np.sum(np.subtract(
            self.hex_centres, np.array([from_position[0], from_position[1]])
        ) ** 2, 1))

    def _nearest_raw_index(self, position):
        '''Zwraca nr rekordu w tabeli pól, który leży najblizej pozycji w px'''
        return self._distances_to_hex(position).argmin()

    def nearest_index(self, position):
        '''Zwraca index hexa, który leży nabliżej pozycji w px'''
        return self.map_indexes[self._nearest_raw_index(position)]

    def nearest_hex_center(self, position):
        '''Zwraca srodek hexa, który leży nabliżej pozycji w px'''
        return self.hex_centres[self._nearest_raw_index(position)]

    def position_on_hex(self, position):
        '''Zwraca True jeżeli pozycja w px znajduje się nad hexem. Dodatkowo zwraca index hexa i jego środek.'''
        distances = self._distances_to_hex(position)
        argm = distances.argmin()
        return distances[argm] < self.hex_a, self.map_indexes[argm], self.hex_centres[argm]

    def hex_draw(self, center, a=None):
        if not a:
            a = self.hex_a
        return (
            (center[0] - a, int(center[1])),
            (center[0] - a / 2.0, int(center[1] + a * sqrt(3) / 2.0)),
            (center[0] + a / 2.0, int(center[1] + a * sqrt(3) / 2.0)),
            (center[0] + a, int(center[1])),
            (center[0] + a / 2.0, int(center[1] - a * sqrt(3) / 2.0)),
            (center[0] - a / 2.0, int(center[1] - a * sqrt(3) / 2.0))
        )

    @property
    def hex_centres(self):
        return self._hex_centres

    @hex_centres.setter
    def hex_centres(self, value):
        self._hex_centres = value

    def _calc_hex_centres(self):
        margin_y = self.hex_margin * sqrt(3) / 2.0
        offset_x = self.hex_a
        offset_y = self.hex_a * sqrt(3) + margin_y / 2.0
        col_offset = min(self.map_cols())
        row_offset = min(self.map_rows())
        self.hex_centres = np.array([
                [offset_x + (col - col_offset) * self.hex_margin +
                (col - col_offset) * 1.5 * self.hex_a,

                offset_y + (row - row_offset) * margin_y +
                (row - row_offset) * self.hex_a * sqrt(3) -
                (col % 2) * (self.hex_a * sqrt(3) / 2.0 + margin_y / 2.0)]

                for col, row in self.map_indexes
            ])

class TestBoardFunctions(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_map_size(self):
        self.board.map = (),
        self.assertEqual(tuple(self.board.map_size), (0, 0))

        self.board.map = (((3 , 2),),)
        self.assertEqual(tuple(self.board.map_size), (1, 1))

        self.board.map = (((0 , 0),),)
        self.assertEqual(tuple(self.board.map_size), (1, 1))

        self.board.map = (((0 , 0),), ((2, 0),))
        self.assertEqual(tuple(self.board.map_size), (3, 1))

        self.board.map = (((0 , 0),), ((0, 5),))
        self.assertEqual(tuple(self.board.map_size), (1, 6))

        self.board.map = (((0 , 0),), ((1, 1),))
        self.assertEqual(tuple(self.board.map_size), (2, 1.5))

        self.board.map = (((0 , 0),), ((10, 5),), ((9, 6),))
        self.assertEqual(tuple(self.board.map_size), (11, 6.5))

    def test_mouse_click(self):
        self.board.hex_margin = 10
        self.board.map = maps.STANDARD
        for center in self.board.hex_centres:
            #sprawdzamy czy jak klikamy w srodek hexa na planszy to czy faktycznie funkcja zwraca ze kliknielismy hexa
            self.assertTrue(self.board.position_on_hex(center)[0])

        for center in self.board.hex_centres:
            #sprawdzamy czy jak klikamy w srodek hexa na planszy to czy faktycznie funkcja zwraca prawidlowy srodek hexa
            self.assertTrue((self.board.position_on_hex(center)[2] == center).all())

        for center in self.board.hex_centres:
            #sprawdzamy czy jak klikamy w krawedzie hexa na planszy to czy faktycznie funkcja zwraca prawidlowy srodek hexa
            self.assertTrue((self.board.position_on_hex((center[0] + self.board.hex_a - 1, center[1]))[2] == center).all())
            self.assertTrue((self.board.position_on_hex((center[0] - self.board.hex_a + 1, center[1]))[2] == center).all())

        for center in self.board.hex_centres:
            #sprawdzamy czy jak klikamy tuż za krawędzia to czy funkcja zwróci false
            self.assertFalse((self.board.position_on_hex((center[0] + self.board.hex_a + 1, center[1]))[0]))
            self.assertFalse((self.board.position_on_hex((center[0] - self.board.hex_a - 1, center[1]))[0]))



if __name__ == '__main__':
    unittest.main()
