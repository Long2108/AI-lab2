"""Input parser for the CSV format required by the lab specification."""

from typing import List, Tuple


def _clean_lines(filename: str) -> List[str]:
    lines = []
    with open(filename, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].strip()
            if line:
                lines.append(line)
    return lines


def _parse_csv_ints(line: str, expected_len: int, section: str) -> List[int]:
    values = [int(x.strip()) for x in line.split(",") if x.strip()]
    if len(values) != expected_len:
        raise ValueError(f"{section} must contain {expected_len} comma-separated integers: {line}")
    return values


def _validate_constraint_rows(rows: List[List[int]], section: str) -> None:
    for row in rows:
        for value in row:
            if value not in (-1, 0, 1):
                raise ValueError(f"{section} constraints must be -1, 0, or 1")


def read_input(filename: str) -> Tuple[int, List[List[int]], List[List[int]], List[List[int]]]:
    """Read a Futoshiki input file.

    Format:
    - N
    - N grid rows, each with N comma-separated values
    - N horizontal-constraint rows, each with N-1 values
    - N-1 vertical-constraint rows, each with N values
    """
    lines = _clean_lines(filename)
    if not lines:
        raise ValueError("Input file is empty")

    N = int(lines[0])
    if N <= 0:
        raise ValueError("N must be positive")

    expected = 1 + N + N + (N - 1)
    if len(lines) < expected:
        raise ValueError(f"Input has {len(lines)} data lines; expected at least {expected}")

    idx = 1
    grid = []
    for _ in range(N):
        row = _parse_csv_ints(lines[idx], N, "Grid")
        if any(value < 0 or value > N for value in row):
            raise ValueError(f"Grid values must be in range 0..{N}")
        grid.append(row)
        idx += 1

    h_cons = []
    for _ in range(N):
        h_cons.append(_parse_csv_ints(lines[idx], N - 1, "Horizontal"))
        idx += 1

    v_cons = []
    for _ in range(N - 1):
        v_cons.append(_parse_csv_ints(lines[idx], N, "Vertical"))
        idx += 1

    _validate_constraint_rows(h_cons, "Horizontal")
    _validate_constraint_rows(v_cons, "Vertical")

    return N, grid, h_cons, v_cons
