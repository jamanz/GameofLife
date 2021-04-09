from contracts import contract, new_contract, check_multiple
import os
import numpy as np
import unittest, os, copy
from itertools import product


def read_file(input_file:str):
    """
    :param input_file:
    :return: generations: int, width: int, height: int, board_2d: list[list[str]]
    """
    with open(input_file, 'r') as f:
        generations = f.readline()
        width, height = f.readline().split()
        board_2d = [[el for el in row] for row in f.read().split('\n')]
        try:
            generations = int(generations)
            width = int(width)
            height = int(height)
        except ValueError:
            print(f'Ensure that input values are numbers  {input_file}')
    return generations, width, height, board_2d


def board_is_valid(width, height, board_2d):
    board_valid_symbols = ('.', 'x')

    if len(board_2d[0]) != width:
        msg = f'Input board width {width} doesnt match with number of board columns {len(board_2d[0])}'
        raise ValueError(msg)
    elif len(board_2d) != height:
        msg = f'Input board height {height} doesnt match with actual board rows {len(board_2d)}'
        raise ValueError(msg)

    for row in board_2d:
        for el in row:
            if el not in board_valid_symbols:
                msg = 'Allowed symbols in boad:\n . - cell is dead\n x - cell is alive'
                raise ValueError(msg)
    return True


class TestGame(unittest.TestCase):
    def test_board_is_valid(self):
        cases = (
            [1, 1, [['x']]],
            [1, 1, [['']]]
        )
        for c in cases:
            with self.subTest(case=c):
                params = c
                self.assertTrue()


def cell_neighborhood(x, y, board_2d):
    neibors_filter = [
        [(-1, -1), (-1, 0), (-1, 1)],
        [(0, -1), (0, 0), (0, 1)],
        [(1, -1), (1, 0), (1, 1)]
    ]
    nb_values_stride = []
    nb_coord_stride = []
    for lvl in neibors_filter:
        row_val = []
        row_coord = []
        for pair in lvl:
            nb_coord_x = x + pair[0]
            nb_coord_y = y + pair[1]
            if nb_coord_x > len(board_2d) - 1:
                nb_coord_x = 0
            if nb_coord_y > len(board_2d[0]) - 1:
                nb_coord_y = 0
            row_val.append(board_2d[nb_coord_x][nb_coord_y])
            row_coord.append((nb_coord_x, nb_coord_y))
        nb_values_stride.append(row_val)
        nb_coord_stride.append(row_coord)
    # print(*nb_values_stride, sep='\n')
    # print(*nb_coord_stride, sep='\n')
    return nb_values_stride, nb_coord_stride


def next_gen_cell(x, y, board_2d):
    neighbor_count = 0
    nd_values, nd_coords = cell_neighborhood(x, y, board_2d)
    isAlive = 0
    core_cell = nd_values[1][1]
    # print('core check is : ', core_cell)
    if core_cell == 'x':
        #check rules for alive
        for nb_val_row, nb_coord_row in zip(nd_values, nd_coords):
            for cell_val, cell_coord in zip(nb_val_row, nb_coord_row):
                if cell_coord == (x, y):
                    # print(f'val on cont {cell_val}')
                    continue
                if cell_val == 'x':
                    neighbor_count += 1


        if neighbor_count in (2, 3):
            isAlive = True
        if neighbor_count < 2:
            isAlive = False
        elif neighbor_count > 3:
            isAlive = False
        # print(f'cell[{x}][{y}] neibor count: {neighbor_count} isAlive: {isAlive}')
        if isAlive:
            return 'x'
        else:
            return '.'
    elif core_cell == '.':
        #check rules for dead
        for nb_val_row, nb_coord_row in zip(nd_values, nd_coords):
            for cell_val, cell_coord in zip(nb_val_row, nb_coord_row):
                if cell_coord == (x, y):
                    # skip core_cell
                    continue
                if cell_val == 'x':
                    neighbor_count += 1


        # print(f'cell[{x}][{y}] neibor count: {neighbor_count}')
        if neighbor_count == 3:
            return 'x'
        return '.'


def print_board(board_2d):
    for row in board_2d:
        print(*row, sep='')

def run_generation(board_2d):
    new_gen = copy.deepcopy(board_2d)
    for i, row in enumerate(board_2d):
        for j, cell in enumerate(row):
            new_gen[i][j] = next_gen_cell(i, j, board_2d)
            # print(f'{new_gen[i][j]}')
    return new_gen



generations, width, height, board_2d = read_file('tes.txt')
if board_is_valid(width, height, board_2d):
    all_generations = {
        '0': board_2d
    }
    for gen in range(generations):
        all_generations[f'{gen + 1}'] = run_generation(all_generations[f'{gen}'])
        print('GEN: ', gen+1)
        print_board(all_generations[f'{gen + 1}'])




