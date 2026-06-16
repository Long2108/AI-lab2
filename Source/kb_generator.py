"""Ground knowledge-base generator for Futoshiki."""
from typing import Dict, List, Tuple


Fact = Tuple


def generate_kb(N: int, grid=None, h_cons=None, v_cons=None) -> Dict[str, List[Fact]]:
    facts: List[Fact] = []
    domains: List[Fact] = []
    rules: List[Fact] = []

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            for v in range(1, N + 1):
                domains.append(("Candidate", i, j, v))

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

    return {"facts": facts, "domains": domains, "rules": rules}


if __name__ == '__main__':
    print('KB generator skeleton: generate_kb(N)')
