"""Forward-chaining style constraint propagation for Futoshiki."""

from copy import deepcopy
from typing import Dict, List, Optional, Set, Tuple

from constraints import domain_values, is_complete, is_valid_grid
from logic import HornRule, Var, forward_chain_horn
from metrics import SolverResult, SolverStats

Fact = Tuple


def _initial_domains(N: int, grid, h_cons, v_cons) -> Dict[Tuple[int, int], Set[int]]:
    domains = {}
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 0:
                domains[(r, c)] = domain_values(grid, r, c, h_cons, v_cons)
            else:
                domains[(r, c)] = {grid[r][c]}
    return domains


def _propagate(N: int, grid, h_cons, v_cons) -> Tuple[bool, Set[Fact]]:
    """Apply deterministic rules until no new Val/NotVal facts appear."""
    known: Set[Fact] = set()
    changed = True

    while changed:
        changed = False
        domains = _initial_domains(N, grid, h_cons, v_cons)

        for (r, c), values in domains.items():
            if not values:
                return False, known | {("Contradiction", r + 1, c + 1)}
            for value in range(1, N + 1):
                if value not in values:
                    known.add(("NotVal", r + 1, c + 1, value))
            if grid[r][c] == 0 and len(values) == 1:
                value = next(iter(values))
                grid[r][c] = value
                known.add(("Val", r + 1, c + 1, value))
                changed = True

        for unit in range(N):
            for value in range(1, N + 1):
                row_cells = [(unit, c) for c in range(N) if grid[unit][c] == 0 and value in domains[(unit, c)]]
                if not any(grid[unit][c] == value for c in range(N)) and len(row_cells) == 1:
                    r, c = row_cells[0]
                    grid[r][c] = value
                    known.add(("Val", r + 1, c + 1, value))
                    changed = True

                col_cells = [(r, unit) for r in range(N) if grid[r][unit] == 0 and value in domains[(r, unit)]]
                if not any(grid[r][unit] == value for r in range(N)) and len(col_cells) == 1:
                    r, c = col_cells[0]
                    grid[r][c] = value
                    known.add(("Val", r + 1, c + 1, value))
                    changed = True

        if not is_valid_grid(grid, h_cons, v_cons):
            return False, known | {("Contradiction",)}

    return True, known


def forward_chaining(facts: Set[Fact], rules: List) -> Set[Fact]:
    """Generic forward chaining over callable Horn rules."""
    changed = True
    known = set(facts)
    while changed:
        changed = False
        for rule in rules:
            for fact in rule(known):
                if fact not in known:
                    known.add(fact)
                    changed = True
    return known


def puzzle_facts(N: int, grid: List[List[int]], h_cons, v_cons) -> Set[Fact]:
    facts: Set[Fact] = set()
    for value in range(1, N + 1):
        facts.add(("Number", value))
    for r in range(N):
        for c in range(N):
            facts.add(("Cell", r + 1, c + 1))
            if grid[r][c] != 0:
                facts.add(("Given", r + 1, c + 1, grid[r][c]))
    for r, row in enumerate(h_cons, 1):
        for c, sign in enumerate(row, 1):
            if sign == 1:
                facts.add(("LessH", r, c))
            elif sign == -1:
                facts.add(("GreaterH", r, c))
    for r, row in enumerate(v_cons, 1):
        for c, sign in enumerate(row, 1):
            if sign == 1:
                facts.add(("LessV", r, c))
            elif sign == -1:
                facts.add(("GreaterV", r, c))
    return facts


def puzzle_rules() -> List[HornRule]:
    i = Var("i")
    j = Var("j")
    v = Var("v")
    return [
        HornRule((("Given", i, j, v),), ("Val", i, j, v), "given-implies-value"),
        HornRule((("LessH", i, j),), ("HasConstraint", i, j), "horizontal-less-constraint"),
        HornRule((("GreaterH", i, j),), ("HasConstraint", i, j), "horizontal-greater-constraint"),
        HornRule((("LessV", i, j),), ("HasConstraint", i, j), "vertical-less-constraint"),
        HornRule((("GreaterV", i, j),), ("HasConstraint", i, j), "vertical-greater-constraint"),
    ]


def solve_forward_chaining_result(N: int, grid: List[List[int]], h_cons, v_cons) -> SolverResult:
    """Solve by repeated forward propagation, branching only when propagation stalls."""
    work = deepcopy(grid)
    stats = SolverStats("forward")
    horn_facts, horn_inferences = forward_chain_horn(puzzle_facts(N, grid, h_cons, v_cons), puzzle_rules())
    stats.inferences += horn_inferences

    def search(g) -> Optional[List[List[int]]]:
        stats.nodes_expanded += 1
        consistent, _ = _propagate(N, g, h_cons, v_cons)
        if not consistent:
            stats.contradictions += 1
            return None
        if is_complete(g):
            return deepcopy(g) if is_valid_grid(g, h_cons, v_cons, complete=True) else None

        best = None
        best_domain = None
        for r in range(N):
            for c in range(N):
                if g[r][c] == 0:
                    values = domain_values(g, r, c, h_cons, v_cons)
                    if best is None or len(values) < len(best_domain):
                        best = (r, c)
                        best_domain = values
        if best is None:
            return None

        r, c = best
        for value in sorted(best_domain):
            stats.assignments_tried += 1
            child = deepcopy(g)
            child[r][c] = value
            result = search(child)
            if result is not None:
                return result
        return None

    result = search(work)
    stats.inferences += len(infer_facts(N, result, h_cons, v_cons)) if result is not None else len(horn_facts)
    return SolverResult(result, stats)


def solve_forward_chaining(N: int, grid: List[List[int]], h_cons, v_cons) -> Optional[List[List[int]]]:
    return solve_forward_chaining_result(N, grid, h_cons, v_cons).grid


def infer_facts(N: int, grid: List[List[int]], h_cons, v_cons) -> Set[Fact]:
    work = deepcopy(grid)
    _, facts = _propagate(N, work, h_cons, v_cons)
    for r in range(N):
        for c in range(N):
            if work[r][c] != 0:
                facts.add(("Val", r + 1, c + 1, work[r][c]))
    return facts


if __name__ == "__main__":
    print("Forward chaining module. Use solve_forward_chaining(...).")
