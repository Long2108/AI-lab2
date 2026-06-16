from parser import read_input

N, grid, h_cons, v_cons = read_input("Inputs/input-01.txt")

print("N =", N)
print("Grid:")
for row in grid:
    print(row)

print("\nHorizontal:")
for row in h_cons:
    print(row)

print("\nVertical:")
for row in v_cons:
    print(row)
