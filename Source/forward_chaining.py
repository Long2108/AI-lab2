"""Simple forward chaining skeleton for facts and Horn rules."""
from typing import List, Tuple, Set

# Represent facts as tuples like ("Val", i, j, v) or ("Given", i, j, v)
# Represent rules as functions or as simple patterns; here we provide a minimal mechanism.


def forward_chaining(facts: Set[Tuple], rules: List) -> Set[Tuple]:
    changed = True
    known = set(facts)
    while changed:
        changed = False
        for rule in rules:
            new_facts = rule(known)
            for f in new_facts:
                if f not in known:
                    known.add(f)
                    changed = True
    return known


if __name__ == '__main__':
    print('Forward chaining skeleton: implement rules as callables returning new facts given known facts')
