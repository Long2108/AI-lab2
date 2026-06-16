"""Backtracking solver for Futoshiki using parser + constraints."""
from copy import deepcopy
from typing import List, Optional
from constraints import is_valid_placement


def find_empty(grid: List[List[int]]):
    N = len(grid)
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 0:
                return r, c
    return None


def solve_backtracking(N: int, grid: List[List[int]], h_cons, v_cons, limit_solutions=1) -> Optional[List[List[int]]]:
    solutions = []

    def backtrack(g):
        if len(solutions) >= limit_solutions:
            return True
        pos = find_empty(g)
        if not pos:
            solutions.append(deepcopy(g))
            return True
        r, c = pos
        for v in range(1, N + 1):
            if is_valid_placement(g, r, c, v, h_cons, v_cons):
                g[r][c] = v
                backtrack(g)
                g[r][c] = 0
        return False

    backtrack(deepcopy(grid))
    return solutions[0] if solutions else None


if __name__ == '__main__':
    print('Backtracking solver module. Use solve_backtracking(...)')
