"""Utility helpers: printing and saving boards."""
from typing import List


def print_board(grid: List[List[int]]):
    for row in grid:
        print(' '.join(str(v) if v != 0 else '.' for v in row))


def save_board(path: str, grid: List[List[int]]):
    with open(path, 'w', encoding='utf-8') as f:
        for row in grid:
            f.write(' '.join(str(v) if v != 0 else '.' for v in row) + '\n')


if __name__ == '__main__':
    print('utils: print_board, save_board')
