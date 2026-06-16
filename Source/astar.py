"""A* solver skeleton for Futoshiki."""
import heapq
from copy import deepcopy
from typing import List, Optional, Tuple
from Source.constraints import is_valid_placement


def heuristic_count_empty(grid: List[List[int]]) -> int:
    return sum(1 for r in grid for c in r if c == 0)


def solve_astar(N: int, grid: List[List[int]], h_cons, v_cons) -> Optional[List[List[int]]]:
    # State representation: tuple of cells row-major
    start = tuple(cell for row in grid for cell in row)

    def assigned_count(state):
        return sum(1 for v in state if v != 0)

    def h(state):
        return N * N - assigned_count(state)

    pq = []
    heapq.heappush(pq, (h(start), start))
    visited = set()

    while pq:
        f, state = heapq.heappop(pq)
        if state in visited:
            continue
        visited.add(state)
        # reconstruct grid
        cur_grid = [list(state[i * N:(i + 1) * N]) for i in range(N)]
        if all(v != 0 for v in state):
            return cur_grid
        # pick cell with smallest domain
        best = None
        best_dom = None
        for r in range(N):
            for c in range(N):
                if cur_grid[r][c] == 0:
                    dom = [v for v in range(1, N + 1) if is_valid_placement(cur_grid, r, c, v, h_cons, v_cons)]
                    if best is None or len(dom) < best_dom:
                        best = (r, c)
                        best_dom = len(dom)
        if best is None:
            continue
        r, c = best
        dom = [v for v in range(1, N + 1) if is_valid_placement(cur_grid, r, c, v, h_cons, v_cons)]
        for v in dom:
            new = deepcopy(cur_grid)
            new[r][c] = v
            new_state = tuple(cell for row in new for cell in row)
            if new_state in visited:
                continue
            heapq.heappush(pq, (assigned_count(new_state) + h(new_state), new_state))

    return None


if __name__ == '__main__':
    print('A* solver skeleton: solve_astar(N, grid, h_cons, v_cons)')
