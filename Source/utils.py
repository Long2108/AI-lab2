"""Utility helpers: printing and saving boards."""
from typing import List


def format_output(N: int, grid: List[List[int]], h_cons, v_cons) -> str:
    lines = []
    for r in range(N):
        parts = []
        for c in range(N):
            parts.append(str(grid[r][c]))
            if c < N - 1:
                sign = h_cons[r][c]
                parts.append("<" if sign == 1 else ">" if sign == -1 else " ")
        lines.append(" ".join(parts))

        if r < N - 1:
            parts = []
            for c in range(N):
                sign = v_cons[r][c]
                parts.append("^" if sign == 1 else "v" if sign == -1 else " ")
                if c < N - 1:
                    parts.append(" ")
            lines.append(" ".join(parts).rstrip())
    return "\n".join(lines)


def print_board(grid: List[List[int]]):
    for row in grid:
        print(' '.join(str(v) if v != 0 else '.' for v in row))


def save_board(path: str, grid: List[List[int]], h_cons=None, v_cons=None):
    with open(path, 'w', encoding='utf-8') as f:
        if h_cons is not None and v_cons is not None:
            f.write(format_output(len(grid), grid, h_cons, v_cons))
            f.write('\n')
        else:
            for row in grid:
                f.write(' '.join(str(v) if v != 0 else '.' for v in row) + '\n')


if __name__ == '__main__':
    print('utils: print_board, save_board')
