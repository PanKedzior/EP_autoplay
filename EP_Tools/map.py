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
        self.red_points = 0
        self.blue_points = 0
        self.green_points = 0
        self.yellow_points = 0
        self.purple_points = 0
        self.points = [self.red_points, self.blue_points, self.green_points, self.yellow_points, self.purple_points]
        self.randomize_table()
        self.print_table()
        self.check_for_combos()

    def upgrade_points(self):
        self.red_points = self.points[0]
        self.blue_points = self.points[1]
        self.green_points = self.points[2]
        self.yellow_points = self.points[3]
        self.purple_points = self.points[4]

    def print_table(self):
        printed_table = copy.copy(self.table)
        for i, row in enumerate(printed_table):
            for j, diamond in enumerate(row):
                if type(diamond) is Diamond:
                    # printed_table[i][j] = str(self.substitute['Color'][self.substitute['Number'] == diamond.color].iloc[0])
                    printed_table[i][j] = str(diamond.color)
                    if diamond.x4:
                        printed_table[i][j]+='.x4'
                    elif diamond.x5:
                        printed_table[i][j]+='.x5'
        print(printed_table)

    def randomize_table(self):
        self.table = np.array([[Diamond(np.random.randint(1, 5), x, y) for x in range(self.__x_size)] for y in range(self.__y_size)])
        while self.check_for_combos():
            self.table = np.array([[Diamond(np.random.randint(1, 5), x, y) for x in range(self.__x_size)] for y in range(self.__y_size)])
        self.points = [0, 0, 0, 0, 0]

    def move_left(self, x, y):
        self.moves += 1
        assert x != 0, 'The leftmost block cannot be moved left'
        self.table[y][x].was_moved = True
        self.table[y][x-1].was_moved = True
        self.table[y][x-1], self.table[y][x] = self.table[y][x], self.table[y][x-1]
        self.table[y][x].x_position += 1
        self.table[y][x-1].x_position -= 1
        response = self.check_for_combos()

    def move_right(self, x, y):
        self.moves += 1
        assert x != self.__x_size-1, 'The rightmost block cannot be moved right'
        self.table[y][x].was_moved = True
        self.table[y][x+1].was_moved = True
        self.table[y][x+1], self.table[y][x] = self.table[y][x], self.table[y][x+1]
        self.table[y][x].x_position -= 1
        self.table[y][x+1].x_position += 1
        response = self.check_for_combos()

    def move_up(self, x, y):
        self.moves += 1
        assert y != 0, 'The topmost block cannot be moved up'
        self.table[y][x].was_moved = True
        self.table[y-1][x].was_moved = True
        self.table[y-1][x], self.table[y][x] = self.table[y][x], self.table[y-1][x]
        self.table[y][x].y_position += 1
        self.table[y-1][x].y_position -= 1
        response = self.check_for_combos()

    def move_down(self, x, y):
        self.moves += 1
        assert y != self.__y_size-1, 'The bottommost block cannot be moved down'
        self.table[y][x].was_moved = True
        self.table[y+1][x].was_moved = True
        self.table[y+1][x], self.table[y][x] = self.table[y][x], self.table[y+1][x]
        self.table[y][x].y_position -= 1
        self.table[y+1][x].y_position += 1
        response = self.check_for_combos()

    def push_special_diamond(self, diamond: Diamond):
        self.moves += 1
        assert any([diamond.x4, diamond.x5]), 'Cannot push non special diamond'
        diamond.in_combo = False
        if diamond.x4:
            self.explode(self.get_diamonds_list_on_use_x4(diamond))
        else:
            self.explode(self.get_diamonds_list_on_use_x5(diamond))

    def get_diamonds_list_on_use_x4(self, special_diamond: Diamond):
        x, y = special_diamond.x_position, special_diamond.y_position
        diamonds_to_explode = [special_diamond]
        if x != 0:
            diamonds_to_explode.append(self.table[y][x-1])
        if x != self.__x_size-1:
            diamonds_to_explode.append(self.table[y][x+1])
        if y != 0:
            diamonds_to_explode.append(self.table[y-1][x])
        if y != self.__y_size-1:
            diamonds_to_explode.append(self.table[y+1][x])
        return diamonds_to_explode

    def get_diamonds_list_on_use_x5(self, special_diamond: Diamond):
        diamonds_to_explode = []
        for row_number, row in enumerate(self.table):
            for column_number, diamond in enumerate(row):
                if diamond.color == special_diamond.color:
                    diamonds_to_explode.append(diamond)
        return diamonds_to_explode

    def move_diamonds_after_explosion(self):
        for row_number, row in enumerate(self.table[1:]):
            row_number += 1
            for column_number, diamond in enumerate(row):
                if diamond is np.nan:
                    continue
                i = 0
                while row_number - 1 - i >= 0 and self.table[row_number - 1 - i][column_number] is np.nan:
                    self.table[row_number - i][column_number].y_position -= 1
                    self.table[row_number - 1 - i][column_number] = self.table[row_number - i][column_number]
                    self.table[row_number - i][column_number] = np.nan
                    i += 1
        # self.print_table()
        self.generate_new_diamonds()

    def generate_new_diamonds(self):
        for row_number, row in enumerate(self.table):
            for column_number, diamond in enumerate(row):
                if diamond is np.nan:
                    self.table[row_number][column_number] = Diamond(np.random.randint(1, 5), column_number, row_number)
                else:
                    diamond.was_moved = False
                    diamond.check_vertically = True
                    diamond.check_horizontally = True
                    diamond.in_combo = False
        # self.print_table()
        self.check_for_combos()

    def explode(self, diamonds: list[Diamond]):
        for diamond in diamonds:
            self.points[diamond.color] += 1
            if not diamond.in_combo:
                self.table[diamond.y_position][diamond.x_position] = np.nan
        # self.print_table()
        self.move_diamonds_after_explosion()
        self.check_for_combos()

    def check_for_combos(self):  # TODO add finding x5 on zigzag combo
        combos_made = False
        diamonds_to_explode = set()
        for row_number, row in enumerate(self.table):
            for column_number, diamond in enumerate(row):
                if row_number < self.__y_size:
                    combo_length_horizontally = 1
                    combo_length_vertically = 1
                    if diamond.check_horizontally:
                        for right_neighbor_number in range(row_number+1, self.__y_size):
                            if diamond.color == self.table[right_neighbor_number][column_number].color:
                                combo_length_horizontally += 1
                            else:
                                break
                        if combo_length_horizontally >= 3:
                            # print('found horizontally length ', combo_length_horizontally)
                            # print('starts in row: ', row_number, 'column: ', column_number)
                            combos_made = True
                            for i in range(combo_length_horizontally):
                                self.points[diamond.color] += 1
                                self.table[row_number + i][column_number].check_horizontally = False
                                if self.table[row_number+i][column_number].x4:
                                    additional_diamonds = self.get_diamonds_list_on_use_x4(self.table[row_number + i][column_number])
                                elif self.table[row_number + i][column_number].x5:
                                    additional_diamonds = self.get_diamonds_list_on_use_x5(self.table[row_number + i][column_number])
                                if self.table[row_number + i][column_number].was_moved and combo_length_horizontally == 4:
                                    self.table[row_number + i][column_number].upgrade_x4()
                                    self.table[row_number + i][column_number].in_combo = True
                                elif self.table[row_number + i][column_number].was_moved and combo_length_horizontally > 4:
                                    self.table[row_number + i][column_number].upgrade_x5()
                                    self.table[row_number + i][column_number].in_combo = True
                                if 'additional_diamonds' in locals():
                                    for additional_diamons in additional_diamonds:
                                        diamonds_to_explode.add(additional_diamons)
                                diamonds_to_explode.add(self.table[row_number + i][column_number])
                    if diamond.check_vertically:
                        for down_neighbor_number in range(column_number + 1, self.__x_size):
                            if diamond.color == self.table[row_number][down_neighbor_number].color:
                                combo_length_vertically += 1
                            else:
                                break
                        if combo_length_vertically >= 3:
                            # print('found vertically length ', combo_length_vertically)
                            # print('starts in row: ', row_number, 'column: ', column_number)
                            combos_made = True
                            for i in range(combo_length_vertically):
                                self.points[diamond.color] += 1
                                self.table[row_number][column_number + i].check_vertically = False
                                if self.table[row_number][column_number + i].x4:
                                    additional_diamonds = self.get_diamonds_list_on_use_x4(self.table[row_number][column_number + i])
                                elif self.table[row_number][column_number + i].x5:
                                    additional_diamonds = self.get_diamonds_list_on_use_x5(self.table[row_number][column_number + i])
                                if self.table[row_number][column_number + i].was_moved and combo_length_vertically == 4:
                                    self.table[row_number][column_number + i].upgrade_x4()
                                    self.table[row_number][column_number + i].in_combo = True
                                elif self.table[row_number][column_number + i].was_moved and combo_length_vertically > 4:
                                    self.table[row_number][column_number + i].upgrade_x5()
                                    self.table[row_number][column_number + i].in_combo = True
                                diamonds_to_explode.add(self.table[row_number][column_number + i])
                                if 'additional_diamonds' in locals():
                                    for additional_diamons in additional_diamonds:
                                        diamonds_to_explode.add(additional_diamons)
        if combos_made:
            diamonds_to_explode = list(diamonds_to_explode)
            self.explode(diamonds_to_explode)
        return combos_made

start = time.perf_counter()
a = Map()
end = time.perf_counter()
print(end-start)
