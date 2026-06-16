from parser import read_input
from constraints import is_valid

N, grid, h_cons, v_cons = read_input(
    "Inputs/input-01.txt"
)
for v in range(1, N + 1):
    print(
        f"value={v}",
        is_valid(
            grid,
            0,
            0,
            v,
            h_cons,
            v_cons
        )
    )