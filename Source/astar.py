"""A* solver skeleton for Futoshiki."""
import heapq
from copy import deepcopy
from itertools import count
from typing import List, Optional
from constraints import domain_values, is_valid_grid
from metrics import SolverResult, SolverStats


def heuristic_count_empty(grid: List[List[int]]) -> int:
    return sum(1 for r in grid for c in r if c == 0)


def solve_astar_result(N: int, grid: List[List[int]], h_cons, v_cons) -> SolverResult:
    # State representation: tuple of cells row-major
    start = tuple(cell for row in grid for cell in row)
    stats = SolverStats("astar")

    def assigned_count(state):
        return sum(1 for v in state if v != 0)

    def h(state):
        return N * N - assigned_count(state)

    pq = []
    tie = count()
    heapq.heappush(pq, (h(start), 0, next(tie), start))
    visited = set()

    while pq:
        stats.max_frontier = max(stats.max_frontier, len(pq))
        _, g_cost, _, state = heapq.heappop(pq)
        if state in visited:
            continue
        visited.add(state)
        stats.nodes_expanded += 1
        cur_grid = [list(state[i * N:(i + 1) * N]) for i in range(N)]
        if all(v != 0 for v in state):
            if is_valid_grid(cur_grid, h_cons, v_cons, complete=True):
                return SolverResult(cur_grid, stats)
            continue

        best = None
        best_dom = []
        for r in range(N):
            for c in range(N):
                if cur_grid[r][c] == 0:
                    dom = sorted(domain_values(cur_grid, r, c, h_cons, v_cons))
                    if not dom:
                        best = (r, c)
                        best_dom = []
                        break
                    if best is None or len(dom) < len(best_dom):
                        best = (r, c)
                        best_dom = dom
            if best is not None and not best_dom:
                break
        if best is None:
            continue
        if not best_dom:
            continue

        r, c = best
        for v in best_dom:
            stats.assignments_tried += 1
            new = deepcopy(cur_grid)
            new[r][c] = v
            new_state = tuple(cell for row in new for cell in row)
            if new_state in visited:
                continue
            new_g = g_cost + 1
            heapq.heappush(pq, (new_g + h(new_state), new_g, next(tie), new_state))

    return SolverResult(None, stats)


def solve_astar(N: int, grid: List[List[int]], h_cons, v_cons) -> Optional[List[List[int]]]:
    return solve_astar_result(N, grid, h_cons, v_cons).grid


if __name__ == '__main__':
    print('A* solver skeleton: solve_astar(N, grid, h_cons, v_cons)')
