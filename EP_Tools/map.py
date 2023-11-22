import time

import numpy as np
import copy
import pandas as pd
from diamond import Diamond


class Map:
    def __init__(self):
        self.substitute = pd.read_csv('diamonds_colors.csv', delimiter=';')
        self.__x_size = 7
        self.__y_size = 5
        self.moves = 0
        self.randomize_table()
        self.check_for_combos()
        self.print_table()
        # self.move_up(1, 1)
        # self.check_for_combos()
        # self.print_table()

    def print_table(self):
        printed_table = copy.copy(self.table)
        for i, row in enumerate(printed_table):
            for j, value in enumerate(row):
                printed_table[i][j] = str(self.substitute['Color'][self.substitute['Number'] == value.color].iloc[0])
        print(printed_table)

    def randomize_table(self):
        self.table = np.array([[Diamond(np.random.randint(1, 5)) for _ in range(self.__x_size)] for _ in range(self.__y_size)])
        # while self.check_for_combos():
        #     self.table = np.array([[Diamond(np.random.randint(1, 5)) for _ in range(self.__x_size)] for _ in range(self.__y_size)])

    def move_left(self, x, y):
        self.moves += 1
        assert x != 0, 'The leftmost block cannot be moved left'
        self.table[y][x].was_moved = True
        self.table[y][x-1], self.table[y][x] = self.table[y][x], self.table[y][x-1]
        response = self.check_for_combos()

    def move_right(self, x, y):
        self.moves += 1
        assert x != self.__x_size-1, 'The rightmost block cannot be moved right'
        self.table[y][x].was_moved = True
        self.table[y][x+1], self.table[y][x] = self.table[y][x], self.table[y][x+1]
        response = self.check_for_combos()

    def move_up(self, x, y):
        self.moves += 1
        assert y != 0, 'The topmost block cannot be moved up'
        self.table[y][x].was_moved = True
        self.table[y-1][x], self.table[y][x] = self.table[y][x], self.table[y-1][x]
        response = self.check_for_combos()

    def move_down(self, x, y):
        self.moves += 1
        assert y != self.__y_size-1, 'The bottommost block cannot be moved down'
        self.table[y][x].was_moved = True
        self.table[y+1][x], self.table[y][x] = self.table[y][x], self.table[y+1][x]
        response = self.check_for_combos()

    def push(self, diamond: Diamond):
        self.moves += 1
        assert any([diamond.x4, diamond.x5]), 'Cannot push non special diamond'

    def check_for_combos(self):  # TODO add reroll board if check_for_combos_on_start returns True
        start = time.perf_counter()
        combos_made = False
        for row_number, row in enumerate(self.table):
            for column_number, diamond in enumerate(row):
                if row_number < self.__y_size-2 and diamond.check_vertically:
                    combo_length_horizontally = 1
                    combo_length_vertically = 1
                    for neighbor_number in range(row_number+1, self.__y_size):
                        if diamond.color == self.table[neighbor_number][column_number].color:
                            combo_length_horizontally += 1
                            self.table[neighbor_number][column_number].check_vertically = False
                        else:
                            break
                    if combo_length_horizontally >= 3:
                        # print('found horizontally length ', combo_length_horizontally)
                        # print('starts in row: ', row_number, 'column: ', column_number)
                        combos_made = True
                        for i in range(combo_length_horizontally):
                            self.table[row_number+i][column_number].in_combo = True
                            self.table[row_number+i][column_number].check_vertically = False
                        if combo_length_horizontally == 4:
                            diamond.upgrade_x4()
                        elif combo_length_horizontally > 4:
                            diamond.upgrade_x5()
                    for neighbor_number in range(column_number + 1, self.__x_size):
                        if diamond.color == self.table[row_number][neighbor_number].color:
                            combo_length_vertically += 1
                            self.table[row_number][neighbor_number].check_horizontally = False
                        else:
                            break
                    if combo_length_vertically >= 3:
                        # print('found vertically length ', combo_length_vertically)
                        # print('starts in row: ', row_number, 'column: ', column_number)
                        combos_made = True
                        for i in range(combo_length_vertically):
                            self.table[row_number][column_number + i].in_combo = True
                            self.table[row_number][column_number + i].check_horizontally = False
                        if combo_length_vertically == 4:
                            diamond.upgrade_x4()
                        elif combo_length_vertically > 4:
                            diamond.upgrade_x5()
        return combos_made

    def check_for_combos_on_start(self):  # TODO add checking new generated map for combos, returns True if generated map has any arranged row
        pass

Map()