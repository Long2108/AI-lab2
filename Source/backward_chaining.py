"""Backward chaining (SLD-like) queries for Futoshiki values."""

from copy import deepcopy
from typing import List, Optional, Set, Tuple

from constraints import domain_values, is_complete, is_valid_grid
from forward_chaining import puzzle_facts, puzzle_rules
from logic import backward_chain_horn
from metrics import SolverResult, SolverStats

Fact = Tuple


def backward_query(query: Fact, facts: Set[Fact], rules: List = None, depth_limit: int = 50) -> bool:
    """Generic fact query helper kept for report/demo compatibility."""
    if query in facts:
        return True
    if rules is None or depth_limit <= 0:
        return False
    return backward_chain_horn(query, facts, rules, depth_limit)


def query_cell_values(N: int, grid: List[List[int]], h_cons, v_cons, row: int, col: int) -> List[int]:
    """Return all values that can prove Val(row,col,value).

    Public row/col arguments are 1-based to match the FOL notation.
    """
    r = row - 1
    c = col - 1
    if not (0 <= r < N and 0 <= c < N):
        raise ValueError("row and col must be in range 1..N")
    return sorted(domain_values(grid, r, c, h_cons, v_cons))


def solve_backward_chaining_result(N: int, grid: List[List[int]], h_cons, v_cons) -> SolverResult:
    """Solve by recursively proving Val(i,j,v) goals using SLD-style DFS."""
    work = deepcopy(grid)
    stats = SolverStats("backward")
    facts = puzzle_facts(N, grid, h_cons, v_cons)
    rules = puzzle_rules()

    def select_goal(g):
        best = None
        best_values = None
        for r in range(N):
            for c in range(N):
                if g[r][c] == 0:
                    values = query_cell_values(N, g, h_cons, v_cons, r + 1, c + 1)
                    if not values:
                        return (r, c), []
                    if best is None or len(values) < len(best_values):
                        best = (r, c)
                        best_values = values
        return best, best_values

    def prove(g) -> Optional[List[List[int]]]:
        stats.nodes_expanded += 1
        if is_complete(g):
            return deepcopy(g) if is_valid_grid(g, h_cons, v_cons, complete=True) else None
        goal, values = select_goal(g)
        if goal is None or not values:
            stats.contradictions += 1
            return None
        r, c = goal
        for value in values:
            stats.assignments_tried += 1
            stats.inferences += 1
            backward_chain_horn(("Val", r + 1, c + 1, value), facts | {("Given", r + 1, c + 1, value)}, rules)
            child = deepcopy(g)
            child[r][c] = value
            if not is_valid_grid(child, h_cons, v_cons):
                continue
            result = prove(child)
            if result is not None:
                return result
        return None

    return SolverResult(prove(work), stats)


def solve_backward_chaining(N: int, grid: List[List[int]], h_cons, v_cons) -> Optional[List[List[int]]]:
    return solve_backward_chaining_result(N, grid, h_cons, v_cons).grid


if __name__ == "__main__":
    print("Backward chaining module. Use solve_backward_chaining(...).")
