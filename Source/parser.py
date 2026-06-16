def read_input(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    N = int(lines[0])

    idx = 1

    grid = []
    for _ in range(N):
        row = [int(x.strip()) for x in lines[idx].split(",")]
        grid.append(row)
        idx += 1

    h_cons = []
    for _ in range(N):
        row = [int(x.strip()) for x in lines[idx].split(",")]
        h_cons.append(row)
        idx += 1

    v_cons = []
    for _ in range(N - 1):
        row = [int(x.strip()) for x in lines[idx].split(",")]
        v_cons.append(row)
        idx += 1

    return N, grid, h_cons, v_cons
