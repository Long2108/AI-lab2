"""Ground knowledge-base generator for Futoshiki."""
from typing import Dict, List, Tuple


Fact = Tuple


def generate_kb(N: int, grid=None, h_cons=None, v_cons=None) -> Dict[str, List[Fact]]:
    facts: List[Fact] = []
    domains: List[Fact] = []
    rules: List[Fact] = []
    ground_rules: List[Fact] = []

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            for v in range(1, N + 1):
                domains.append(("Candidate", i, j, v))
            ground_rules.append(("AtLeastOneValue", i, j, tuple(("Val", i, j, v) for v in range(1, N + 1))))
            for v1 in range(1, N + 1):
                for v2 in range(v1 + 1, N + 1):
                    ground_rules.append(("AtMostOneValue", ("Val", i, j, v1), ("Val", i, j, v2)))

    if grid is not None:
        for i, row in enumerate(grid, 1):
            for j, value in enumerate(row, 1):
                if value:
                    facts.append(("Given", i, j, value))
                    facts.append(("Val", i, j, value))

    if h_cons is not None:
        for i, row in enumerate(h_cons, 1):
            for j, sign in enumerate(row, 1):
                if sign == 1:
                    facts.append(("LessH", i, j))
                elif sign == -1:
                    facts.append(("GreaterH", i, j))

    if v_cons is not None:
        for i, row in enumerate(v_cons, 1):
            for j, sign in enumerate(row, 1):
                if sign == 1:
                    facts.append(("LessV", i, j))
                elif sign == -1:
                    facts.append(("GreaterV", i, j))

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            rules.append(("ExactlyOneCellValue", i, j))
    for i in range(1, N + 1):
        rules.append(("RowPermutation", i))
        rules.append(("ColumnPermutation", i))
        for v in range(1, N + 1):
            for j1 in range(1, N + 1):
                for j2 in range(j1 + 1, N + 1):
                    ground_rules.append(("RowUnique", ("Val", i, j1, v), ("Val", i, j2, v)))
            for r1 in range(1, N + 1):
                for r2 in range(r1 + 1, N + 1):
                    ground_rules.append(("ColumnUnique", ("Val", r1, i, v), ("Val", r2, i, v)))

    if h_cons is not None:
        for i, row in enumerate(h_cons, 1):
            for j, sign in enumerate(row, 1):
                if sign == 0:
                    continue
                for left in range(1, N + 1):
                    for right in range(1, N + 1):
                        violates = left >= right if sign == 1 else left <= right
                        if violates:
                            ground_rules.append(("InequalityReject", ("Val", i, j, left), ("Val", i, j + 1, right)))

    if v_cons is not None:
        for i, row in enumerate(v_cons, 1):
            for j, sign in enumerate(row, 1):
                if sign == 0:
                    continue
                for top in range(1, N + 1):
                    for bottom in range(1, N + 1):
                        violates = top >= bottom if sign == 1 else top <= bottom
                        if violates:
                            ground_rules.append(("InequalityReject", ("Val", i, j, top), ("Val", i + 1, j, bottom)))

    return {"facts": facts, "domains": domains, "rules": rules, "ground_rules": ground_rules}


if __name__ == '__main__':
    print('KB generator skeleton: generate_kb(N)')
