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