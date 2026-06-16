"""CNF generator for the finite-domain Futoshiki encoding."""
from typing import List, Tuple

Literal = str
Clause = Tuple[Literal, ...]


def val(i: int, j: int, v: int) -> str:
    return f"Val({i},{j},{v})"


def neg(atom: str) -> str:
    return f"~{atom}"


def implication_to_cnf(antecedent: str, consequent: str) -> List[str]:
    # very small helper: A -> B becomes (not A) or B which we return as a string
    return [f"(not {antecedent} or {consequent})"]


def formula_to_cnf(formula: str) -> List[str]:
    return [formula]


def generate_cnf(N: int, grid=None, h_cons=None, v_cons=None) -> List[Clause]:
    """Generate propositional CNF clauses for a Futoshiki instance.

    Each clause is a tuple of literals. Negated literals are prefixed with "~".
    """
    clauses: List[Clause] = []

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            clauses.append(tuple(val(i, j, v) for v in range(1, N + 1)))
            for v1 in range(1, N + 1):
                for v2 in range(v1 + 1, N + 1):
                    clauses.append((neg(val(i, j, v1)), neg(val(i, j, v2))))

    for i in range(1, N + 1):
        for v in range(1, N + 1):
            for j1 in range(1, N + 1):
                for j2 in range(j1 + 1, N + 1):
                    clauses.append((neg(val(i, j1, v)), neg(val(i, j2, v))))

    for j in range(1, N + 1):
        for v in range(1, N + 1):
            for i1 in range(1, N + 1):
                for i2 in range(i1 + 1, N + 1):
                    clauses.append((neg(val(i1, j, v)), neg(val(i2, j, v))))

    if grid is not None:
        for i, row in enumerate(grid, 1):
            for j, value in enumerate(row, 1):
                if value:
                    clauses.append((val(i, j, value),))

    if h_cons is not None:
        for i, row in enumerate(h_cons, 1):
            for j, sign in enumerate(row, 1):
                if sign == 0:
                    continue
                for left in range(1, N + 1):
                    for right in range(1, N + 1):
                        violates = left >= right if sign == 1 else left <= right
                        if violates:
                            clauses.append((neg(val(i, j, left)), neg(val(i, j + 1, right))))

    if v_cons is not None:
        for i, row in enumerate(v_cons, 1):
            for j, sign in enumerate(row, 1):
                if sign == 0:
                    continue
                for top in range(1, N + 1):
                    for bottom in range(1, N + 1):
                        violates = top >= bottom if sign == 1 else top <= bottom
                        if violates:
                            clauses.append((neg(val(i, j, top)), neg(val(i + 1, j, bottom))))

    return clauses


if __name__ == '__main__':
    print('CNF generator skeleton: implement Skolemization and CNF conversion')
