from parser import read_input
from constraints import is_valid, is_valid_placement
from copy import deepcopy

N, grid, h_cons, v_cons = read_input("Inputs/input-01.txt")

print("Grid gốc:")
for row in grid:
    print(row)
print("\nH constraints:")
for row in h_cons:
    print(row)
print("\nV constraints:")
for row in v_cons:
    print(row)

# Kiểm tra xem cell (0,0) có thể có giá trị nào không
print("\n--- Testing cell (0,0) ---")
for v in range(1, N+1):
    result = is_valid(deepcopy(grid), 0, 0, v, h_cons, v_cons)
    print(f"is_valid(0, 0, {v}) = {result}")

# Kiểm tra cell (0,2)
print("\n--- Testing cell (0,2) ---")
for v in range(1, N+1):
    result = is_valid(deepcopy(grid), 0, 2, v, h_cons, v_cons)
    print(f"is_valid(0, 2, {v}) = {result}")
