"""Small Horn-clause engine used by the forward/backward chaining modules."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple

Term = object
Atom = Tuple[object, ...]
Substitution = Dict[str, object]


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class HornRule:
    premises: Tuple[Atom, ...]
    conclusion: Atom
    name: str = ""


def _resolve(term: object, subst: Substitution) -> object:
    while isinstance(term, Var) and term.name in subst:
        term = subst[term.name]
    return term


def unify(pattern: Atom, fact: Atom, subst: Optional[Substitution] = None) -> Optional[Substitution]:
    if len(pattern) != len(fact) or pattern[0] != fact[0]:
        return None
    result = dict(subst or {})
    for left, right in zip(pattern[1:], fact[1:]):
        left = _resolve(left, result)
        right = _resolve(right, result)
        if isinstance(left, Var):
            result[left.name] = right
        elif isinstance(right, Var):
            result[right.name] = left
        elif left != right:
            return None
    return result


def substitute(atom: Atom, subst: Substitution) -> Atom:
    return tuple(_resolve(term, subst) if isinstance(term, Var) else term for term in atom)


def _match_premises(premises: Tuple[Atom, ...], facts: Set[Atom], subst: Optional[Substitution] = None) -> Iterable[Substitution]:
    if not premises:
        yield dict(subst or {})
        return
    first, rest = premises[0], premises[1:]
    first = substitute(first, subst or {})
    for fact in list(facts):
        next_subst = unify(first, fact, subst)
        if next_subst is not None:
            yield from _match_premises(rest, facts, next_subst)


def forward_chain_horn(facts: Set[Atom], rules: List[HornRule], max_iterations: int = 1000) -> Tuple[Set[Atom], int]:
    known = set(facts)
    inference_count = 0
    changed = True
    iterations = 0
    while changed and iterations < max_iterations:
        changed = False
        iterations += 1
        for rule in rules:
            for subst in _match_premises(rule.premises, known):
                conclusion = substitute(rule.conclusion, subst)
                if all(not isinstance(term, Var) for term in conclusion) and conclusion not in known:
                    known.add(conclusion)
                    inference_count += 1
                    changed = True
    return known, inference_count


def backward_chain_horn(
    goal: Atom,
    facts: Set[Atom],
    rules: List[HornRule],
    depth_limit: int = 30,
    seen: Optional[Set[Atom]] = None,
) -> bool:
    if any(unify(goal, fact) is not None for fact in facts):
        return True
    if depth_limit <= 0:
        return False
    seen = set(seen or set())
    if goal in seen:
        return False
    seen.add(goal)
    for rule in rules:
        subst = unify(rule.conclusion, goal)
        if subst is None:
            continue
        if all(backward_chain_horn(substitute(premise, subst), facts, rules, depth_limit - 1, seen) for premise in rule.premises):
            return True
    return False
