"""Backtracking solver for Futoshiki using parser + constraints."""
from copy import deepcopy
from typing import List, Optional, Tuple
from constraints import domain_values, is_valid_grid, is_valid_placement
from metrics import SolverResult, SolverStats


def find_empty(grid: List[List[int]], h_cons, v_cons) -> Optional[Tuple[int, int]]:
    N = len(grid)
    best = None
    best_domain_size = None
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 0:
                size = len(domain_values(grid, r, c, h_cons, v_cons))
                if best is None or size < best_domain_size:
                    best = (r, c)
                    best_domain_size = size
    return best


def solve_bruteforce_result(N: int, grid: List[List[int]], h_cons, v_cons) -> SolverResult:
    """Baseline exhaustive search: fill cells row-major with only local pruning."""
    cells = [(r, c) for r in range(N) for c in range(N) if grid[r][c] == 0]
    work = deepcopy(grid)
    stats = SolverStats("bruteforce")

    def dfs(index: int) -> Optional[List[List[int]]]:
        stats.nodes_expanded += 1
        if index == len(cells):
            return deepcopy(work) if is_valid_grid(work, h_cons, v_cons, complete=True) else None
        r, c = cells[index]
        for value in range(1, N + 1):
            stats.assignments_tried += 1
            if is_valid_placement(work, r, c, value, h_cons, v_cons):
                work[r][c] = value
                result = dfs(index + 1)
                if result is not None:
                    return result
                work[r][c] = 0
        return None

    return SolverResult(dfs(0), stats)


def solve_bruteforce(N: int, grid: List[List[int]], h_cons, v_cons) -> Optional[List[List[int]]]:
    return solve_bruteforce_result(N, grid, h_cons, v_cons).grid


def solve_backtracking_result(N: int, grid: List[List[int]], h_cons, v_cons, limit_solutions=1) -> SolverResult:
    solutions = []
    stats = SolverStats("backtrack")

    def backtrack(g):
        stats.nodes_expanded += 1
        if len(solutions) >= limit_solutions:
            return True
        pos = find_empty(g, h_cons, v_cons)
        if not pos:
            if is_valid_grid(g, h_cons, v_cons, complete=True):
                solutions.append(deepcopy(g))
            return True
        r, c = pos
        for v in sorted(domain_values(g, r, c, h_cons, v_cons)):
            stats.assignments_tried += 1
            g[r][c] = v
            backtrack(g)
            g[r][c] = 0
        return False

    backtrack(deepcopy(grid))
    return SolverResult(solutions[0] if solutions else None, stats)


def solve_backtracking(N: int, grid: List[List[int]], h_cons, v_cons, limit_solutions=1) -> Optional[List[List[int]]]:
    return solve_backtracking_result(N, grid, h_cons, v_cons, limit_solutions).grid


if __name__ == '__main__':
    print('Backtracking solver module. Use solve_backtracking(...)')
