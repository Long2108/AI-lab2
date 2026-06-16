"""Parser for Futoshiki input files.

Input format expected:
- First line: N
- Next N lines: N tokens each (numbers or . for empty)
- Optional lines: constraints in the form `H i j <` or `V i j >` (1-based indices)

Functions:
- read_input(path) -> (N, grid, h_cons, v_cons)

h_cons and v_cons are lists of lists where:
 - h_cons[r][c] = 1 means (r,c) < (r,c+1), -1 means >, 0 means none
 - v_cons[r][c] = 1 means (r,c) < (r+1,c), -1 means >, 0 means none
"""
from typing import List, Tuple


def read_input(path: str) -> Tuple[int, List[List[int]], List[List[int]], List[List[int]]]:
    with open(path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip() and not l.strip().startswith('#')]
    if not lines:
        raise ValueError('Empty input')
    N = int(lines[0])
    grid = [[0] * N for _ in range(N)]
    idx = 1
    for r in range(N):
        parts = lines[idx].split()
        idx += 1
        for c in range(N):
            token = parts[c]
            if token in ('.', '_', '0'):
                grid[r][c] = 0
            else:
                grid[r][c] = int(token)

    # initialize constraint matrices
    h_cons = [[0] * (N - 1) for _ in range(N)]  # horizontal between (r,c) and (r,c+1)
    v_cons = [[0] * N for _ in range(N - 1)]  # vertical between (r,c) and (r+1,c)

    while idx < len(lines):
        parts = lines[idx].split()
        idx += 1
        if len(parts) < 4:
            continue
        typ, i_s, j_s, op = parts[0], parts[1], parts[2], parts[3]
        i = int(i_s) - 1
        j = int(j_s) - 1
        if typ.upper() == 'H' and 0 <= i < N and 0 <= j < N - 1:
            h_cons[i][j] = 1 if op == '<' else (-1 if op == '>' else 0)
        if typ.upper() == 'V' and 0 <= i < N - 1 and 0 <= j < N:
            v_cons[i][j] = 1 if op == '<' else (-1 if op == '>' else 0)

    return N, grid, h_cons, v_cons


if __name__ == '__main__':
    print('Parser module. Use read_input(path) to load puzzles.')
