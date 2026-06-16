import argparse
from pathlib import Path
from Source.futoshiki import Puzzle, Solver


def run_file(path: Path, method: str = 'backtrack'):
    p = Puzzle.from_file(str(path))
    solver = Solver(p)
    if method == 'backtrack':
        sols = solver.solve_backtracking(limit_solutions=1)
        if sols:
            print(sols[0].to_string())
            return sols[0]
        else:
            print('No solution found')
            return None
    elif method == 'astar':
        sol = solver.solve_a_star()
        if sol:
            print(sol.to_string())
            return sol
        else:
            print('No solution found')
            return None
    else:
        raise ValueError('Unknown method')


def main():
    parser = argparse.ArgumentParser(description='Futoshiki solver (starter)')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('--method', choices=['backtrack', 'astar'], default='backtrack')
    parser.add_argument('--output', help='Output file path', default=None)
    args = parser.parse_args()
    sol = run_file(Path(args.input), method=args.method)
    if sol and args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(sol.to_string())


if __name__ == '__main__':
    main()
