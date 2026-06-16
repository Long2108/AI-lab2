"""Constraint checking utilities for Futoshiki."""
from typing import List


def row_has_value(grid: List[List[int]], r: int, v: int) -> bool:
    return v in grid[r]


def col_has_value(grid: List[List[int]], c: int, v: int) -> bool:
    return any(grid[r][c] == v for r in range(len(grid)))


def check_inequalities(grid: List[List[int]], h_cons: List[List[int]], v_cons: List[List[int]]) -> bool:
    N = len(grid)
    # horizontal
    for r in range(N):
        for c in range(N - 1):
            sign = h_cons[r][c]
            a = grid[r][c]
            b = grid[r][c + 1]
            if a != 0 and b != 0:
                if sign == 1 and not (a < b):
                    return False
                if sign == -1 and not (a > b):
                    return False
    # vertical
    for r in range(N - 1):
        for c in range(N):
            sign = v_cons[r][c]
            a = grid[r][c]
            b = grid[r + 1][c]
            if a != 0 and b != 0:
                if sign == 1 and not (a < b):
                    return False
                if sign == -1 and not (a > b):
                    return False
    return True


def is_valid_placement(grid: List[List[int]], r: int, c: int, value: int, h_cons: List[List[int]], v_cons: List[List[int]]) -> bool:
    N = len(grid)
    # check row/col uniqueness
    if row_has_value(grid, r, value):
        return False
    if col_has_value(grid, c, value):
        return False

    # check inequality with left neighbor
    if c - 1 >= 0 and grid[r][c - 1] != 0:
        sign = h_cons[r][c - 1]
        if sign == 1 and not (grid[r][c - 1] < value):
            return False
        if sign == -1 and not (grid[r][c - 1] > value):
            return False
    # with right neighbor
    if c < N - 1 and grid[r][c + 1] != 0:
        sign = h_cons[r][c]
        if sign == 1 and not (value < grid[r][c + 1]):
            return False
        if sign == -1 and not (value > grid[r][c + 1]):
            return False
    # up
    if r - 1 >= 0 and grid[r - 1][c] != 0:
        sign = v_cons[r - 1][c]
        if sign == 1 and not (grid[r - 1][c] < value):
            return False
        if sign == -1 and not (grid[r - 1][c] > value):
            return False
    # down
    if r < N - 1 and grid[r + 1][c] != 0:
        sign = v_cons[r][c]
        if sign == 1 and not (value < grid[r + 1][c]):
            return False
        if sign == -1 and not (value > grid[r + 1][c]):
            return False

    return True


if __name__ == '__main__':
    print('constraints module: provides is_valid_placement and helpers')
