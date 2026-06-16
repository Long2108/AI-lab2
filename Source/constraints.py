from typing import List, Set


def check_row(grid, row, value):
    return value not in grid[row]


def check_col(grid, col, value):
    n = len(grid)

    for r in range(n):
        if grid[r][col] == value:
            return False

    return True


def check_horizontal_constraints(grid, row, h_cons):
    n = len(grid)

    for col in range(n - 1):

        left = grid[row][col]
        right = grid[row][col + 1]

        # bỏ qua nếu chưa gán đủ
        if left == 0 or right == 0:
            continue

        constraint = h_cons[row][col]

        # <
        if constraint == 1:
            if left >= right:
                return False

        # >
        elif constraint == -1:
            if left <= right:
                return False

    return True


def check_vertical_constraints(grid, col, v_cons):
    n = len(grid)

    for row in range(n - 1):

        top = grid[row][col]
        bottom = grid[row + 1][col]

        if top == 0 or bottom == 0:
            continue

        constraint = v_cons[row][col]

        # <
        if constraint == 1:
            if top >= bottom:
                return False

        # >
        elif constraint == -1:
            if top <= bottom:
                return False

    return True


def is_valid(grid, row, col, value, h_cons, v_cons):
    """
    Kiểm tra có thể gán value vào (row,col) hay không
    """

    # hàng
    if not check_row(grid, row, value):
        return False

    # cột
    if not check_col(grid, col, value):
        return False

    # thử gán
    original = grid[row][col]
    grid[row][col] = value

    # kiểm tra constraint ngang của hàng hiện tại
    if not check_horizontal_constraints(grid, row, h_cons):
        grid[row][col] = original
        return False

    # kiểm tra constraint dọc của cột hiện tại
    if not check_vertical_constraints(grid, col, v_cons):
        grid[row][col] = original
        return False

    # khôi phục
    grid[row][col] = original

    return True


def is_valid_placement(grid, row, col, value, h_cons, v_cons):
    """Alias for is_valid function"""
    return is_valid(grid, row, col, value, h_cons, v_cons)


def is_complete(grid: List[List[int]]) -> bool:
    return all(value != 0 for row in grid for value in row)


def domain_values(grid: List[List[int]], row: int, col: int, h_cons, v_cons) -> Set[int]:
    if grid[row][col] != 0:
        return {grid[row][col]}
    n = len(grid)
    return {value for value in range(1, n + 1) if is_valid_placement(grid, row, col, value, h_cons, v_cons)}


def is_valid_grid(grid: List[List[int]], h_cons, v_cons, complete: bool = False) -> bool:
    n = len(grid)
    values = set(range(1, n + 1))

    for row in range(n):
        seen = [value for value in grid[row] if value != 0]
        if len(seen) != len(set(seen)):
            return False
        if complete and set(grid[row]) != values:
            return False

    for col in range(n):
        seen = [grid[row][col] for row in range(n) if grid[row][col] != 0]
        if len(seen) != len(set(seen)):
            return False
        if complete and {grid[row][col] for row in range(n)} != values:
            return False

    for row in range(n):
        if not check_horizontal_constraints(grid, row, h_cons):
            return False
    for col in range(n):
        if not check_vertical_constraints(grid, col, v_cons):
            return False

    if complete and not is_complete(grid):
        return False
    return True
