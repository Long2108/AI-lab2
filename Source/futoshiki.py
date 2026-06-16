import heapq
from copy import deepcopy
from typing import List, Tuple, Set, Dict


class Puzzle:
    def __init__(self, N: int, grid: List[List[int]], lessH=None, greaterH=None, lessV=None, greaterV=None):
        self.N = N
        self.grid = grid
        self.lessH = lessH or set()
        self.greaterH = greaterH or set()
        self.lessV = lessV or set()
        self.greaterV = greaterV or set()

    @staticmethod
    def from_file(path: str) -> 'Puzzle':
        with open(path, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.strip().startswith('#')]
        if not lines:
            raise ValueError('Empty input')
        N = int(lines[0])
        grid = [[0 for _ in range(N)] for _ in range(N)]
        idx = 1
        for r in range(N):
            parts = lines[idx].split()
            idx += 1
            for c in range(N):
                val = parts[c]
                if val == '.' or val == '0' or val == '_':
                    grid[r][c] = 0
                else:
                    grid[r][c] = int(val)
        lessH = set()
        greaterH = set()
        lessV = set()
        greaterV = set()
        # remaining lines are constraints of form: H i j <  or V i j >  (1-based indices)
        while idx < len(lines):
            parts = lines[idx].split()
            idx += 1
            if len(parts) < 4:
                continue
            typ, i_s, j_s, op = parts[0], parts[1], parts[2], parts[3]
            i = int(i_s) - 1
            j = int(j_s) - 1
            if typ.upper() == 'H':
                if op == '<':
                    lessH.add((i, j))
                elif op == '>':
                    greaterH.add((i, j))
            elif typ.upper() == 'V':
                if op == '<':
                    lessV.add((i, j))
                elif op == '>':
                    greaterV.add((i, j))
        return Puzzle(N, grid, lessH, greaterH, lessV, greaterV)

    def copy(self):
        return Puzzle(self.N, deepcopy(self.grid), set(self.lessH), set(self.greaterH), set(self.lessV), set(self.greaterV))

    def is_complete(self) -> bool:
        return all(self.grid[r][c] != 0 for r in range(self.N) for c in range(self.N))

    def assigned_count(self) -> int:
        return sum(1 for r in range(self.N) for c in range(self.N) if self.grid[r][c] != 0)

    def possible_values(self, r: int, c: int) -> Set[int]:
        if self.grid[r][c] != 0:
            return {self.grid[r][c]}
        used = set(self.grid[r])
        used |= {self.grid[i][c] for i in range(self.N)}
        used.discard(0)
        vals = set(range(1, self.N + 1)) - used
        # filter by inequalities with already assigned neighbors
        res = set()
        for v in vals:
            ok = True
            # left neighbor (r, c-1) with H constraint between (r,c-1) and (r,c)
            left = (r, c - 1)
            if c - 1 >= 0:
                if (r, c - 1) in self.lessH and self.grid[r][c - 1] != 0:
                    if not (self.grid[r][c - 1] < v):
                        ok = False
                if (r, c - 1) in self.greaterH and self.grid[r][c - 1] != 0:
                    if not (self.grid[r][c - 1] > v):
                        ok = False
            # current with right neighbor (r,c+1): constraint stored for (r,c)
            if (r, c) in self.lessH and self.grid[r][c + 1] != 0 if c + 1 < self.N else False:
                if not (v < self.grid[r][c + 1]):
                    ok = False
            if (r, c) in self.greaterH and self.grid[r][c + 1] != 0 if c + 1 < self.N else False:
                if not (v > self.grid[r][c + 1]):
                    ok = False
            # up neighbor (r-1, c)
            if r - 1 >= 0:
                if (r - 1, c) in self.lessV and self.grid[r - 1][c] != 0:
                    if not (self.grid[r - 1][c] < v):
                        ok = False
                if (r - 1, c) in self.greaterV and self.grid[r - 1][c] != 0:
                    if not (self.grid[r - 1][c] > v):
                        ok = False
            # current with down neighbor (r,c) constraint stored for (r,c)
            if (r, c) in self.lessV and self.grid[r + 1][c] != 0 if r + 1 < self.N else False:
                if not (v < self.grid[r + 1][c]):
                    ok = False
            if (r, c) in self.greaterV and self.grid[r + 1][c] != 0 if r + 1 < self.N else False:
                if not (v > self.grid[r + 1][c]):
                    ok = False
            if ok:
                res.add(v)
        return res

    def is_valid(self) -> bool:
        # check rows and columns uniqueness and inequalities
        for r in range(self.N):
            seen = set()
            for c in range(self.N):
                v = self.grid[r][c]
                if v == 0:
                    continue
                if v in seen:
                    return False
                seen.add(v)
        for c in range(self.N):
            seen = set()
            for r in range(self.N):
                v = self.grid[r][c]
                if v == 0:
                    continue
                if v in seen:
                    return False
                seen.add(v)
        # inequalities
        for (r, c) in self.lessH:
            if self.grid[r][c] != 0 and self.grid[r][c + 1] != 0:
                if not (self.grid[r][c] < self.grid[r][c + 1]):
                    return False
        for (r, c) in self.greaterH:
            if self.grid[r][c] != 0 and self.grid[r][c + 1] != 0:
                if not (self.grid[r][c] > self.grid[r][c + 1]):
                    return False
        for (r, c) in self.lessV:
            if self.grid[r][c] != 0 and self.grid[r + 1][c] != 0:
                if not (self.grid[r][c] < self.grid[r + 1][c]):
                    return False
        for (r, c) in self.greaterV:
            if self.grid[r][c] != 0 and self.grid[r + 1][c] != 0:
                if not (self.grid[r][c] > self.grid[r + 1][c]):
                    return False
        return True

    def to_string(self) -> str:
        lines = []
        for r in range(self.N):
            lines.append(' '.join(str(self.grid[r][c]) if self.grid[r][c] != 0 else '.' for c in range(self.N)))
        return '\n'.join(lines)


class Solver:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle

    def solve_backtracking(self, limit_solutions=1) -> List[Puzzle]:
        N = self.puzzle.N
        solutions = []

        def find_unassigned(grid: List[List[int]]):
            best = None
            best_dom = None
            for r in range(N):
                for c in range(N):
                    if grid[r][c] == 0:
                        p = self.puzzle.possible_values(r, c)
                        if best is None or len(p) < best_dom:
                            best = (r, c)
                            best_dom = len(p)
            return best

        def backtrack(grid: List[List[int]]):
            if len(solutions) >= limit_solutions:
                return
            # find unassigned
            ua = None
            for r in range(N):
                for c in range(N):
                    if grid[r][c] == 0:
                        ua = (r, c)
                        break
                if ua:
                    break
            if not ua:
                sol = Puzzle(N, deepcopy(grid), set(self.puzzle.lessH), set(self.puzzle.greaterH), set(self.puzzle.lessV), set(self.puzzle.greaterV))
                solutions.append(sol)
                return
            r, c = ua
            vals = self.puzzle.possible_values(r, c)
            for v in sorted(vals):
                grid[r][c] = v
                if self.puzzle.is_valid():
                    backtrack(grid)
                grid[r][c] = 0

        backtrack(deepcopy(self.puzzle.grid))
        return solutions

    def solve_a_star(self) -> Puzzle:
        # simple A* where g = assigned count, h = remaining unassigned cells
        start = self.puzzle
        N = start.N
        start_state = tuple(cell for row in start.grid for cell in row)
        def assigned_count(state):
            return sum(1 for v in state if v != 0)

        def h(state):
            return N * N - assigned_count(state)

        pq = []
        g_scores = {start_state: 0}
        heapq.heappush(pq, (h(start_state), start_state))
        came_from = {}
        visited = set()
        while pq:
            f, state = heapq.heappop(pq)
            if state in visited:
                continue
            visited.add(state)
            # reconstruct puzzle object
            grid = [list(state[i * N:(i + 1) * N]) for i in range(N)]
            cur = Puzzle(N, grid, set(start.lessH), set(start.greaterH), set(start.lessV), set(start.greaterV))
            if cur.is_complete() and cur.is_valid():
                return cur
            # choose a cell with smallest domain
            best = None
            best_dom = None
            for r in range(N):
                for c in range(N):
                    if grid[r][c] == 0:
                        # temporarily set puzzle grid for domain calc
                        self.puzzle.grid = grid
                        dom = self.puzzle.possible_values(r, c)
                        if best is None or len(dom) < best_dom:
                            best = (r, c)
                            best_dom = len(dom)
            if best is None:
                continue
            r, c = best
            self.puzzle.grid = grid
            dom = self.puzzle.possible_values(r, c)
            for v in dom:
                new_grid = deepcopy(grid)
                new_grid[r][c] = v
                new_state = tuple(cell for row in new_grid for cell in row)
                if new_state in visited:
                    continue
                g = assigned_count(new_state)
                fscore = g + h(new_state)
                if new_state not in g_scores or g < g_scores[new_state]:
                    g_scores[new_state] = g
                    came_from[new_state] = state
                    heapq.heappush(pq, (fscore, new_state))
        return None


if __name__ == '__main__':
    print('This module provides Puzzle and Solver classes. Run from repo root with: python -m Source.main')
