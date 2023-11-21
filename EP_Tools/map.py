import numpy as np
import random
import copy
import pandas as pd
from diamond import Diamond


class Map:
    def __init__(self):
        self.substitute = pd.read_csv('diamonds_colors.csv', delimiter=';')
        self.__x_size = 7
        self.__y_size = 5
        self.moves = 0
        self.table = self.randomize_table()
        self.check_first_table()

    def print_table(self):
        printed_table = copy.copy(self.table)
        for i, row in enumerate(printed_table):
            for j, value in enumerate(row):
                printed_table[i][j] = str(self.substitute['Color'][self.substitute['Number'] == value.color].iloc[0])
        print(printed_table)

    def randomize_table(self):
        table = np.array([[Diamond(random.randint(1, 5)) for _ in range(self.__x_size)] for _ in range(self.__y_size)])
        return table

    def move_left(self, x, y):
        self.moves += 1
        assert x != 0, 'The leftmost block cannot be moved left'
        self.table[y][x-1], self.table[y][x] = self.table[y][x], self.table[y][x-1]

    def move_right(self, x, y):
        self.moves += 1
        assert x != self.__x_size-1, 'The rightmost block cannot be moved right'
        self.table[y][x+1], self.table[y][x] = self.table[y][x], self.table[y][x+1]

    def move_up(self, x, y):
        self.moves += 1
        assert y != 0, 'The topmost block cannot be moved up'
        self.table[y-1][x], self.table[y][x] = self.table[y][x], self.table[y-1][x]

    def move_down(self, x, y):
        self.moves += 1
        assert y != self.__y_size-1, 'The bottommost block cannot be moved down'
        self.table[y+1][x], self.table[y][x] = self.table[y][x], self.table[y+1][x]

    def push(self, diamond: Diamond):
        self.moves += 1
        assert any([diamond.x4, diamond.x5]), 'Cannot push non special diamond'

    def check_first_table(self):  # TODO add reroll board if check_for_combos_on_start returns True
        pass

    def check_for_combos_on_start(self):  # TODO add checking new generated map for combos, returns True if generated map has any arranged row
        pass

