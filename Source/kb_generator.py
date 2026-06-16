"""Knowledge-base generator for ground Val/Given atoms."""
from typing import List


def generate_kb(N: int) -> List[str]:
    kb = []
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            for v in range(1, N + 1):
                kb.append(f"Val({i},{j},{v})")
    return kb


if __name__ == '__main__':
    print('KB generator skeleton: generate_kb(N)')
