import argparse
import os
import time

from astar import solve_astar
from backtracking import solve_backtracking, solve_bruteforce
from backward_chaining import solve_backward_chaining
from cnf_generator import generate_cnf
from forward_chaining import infer_facts, solve_forward_chaining
from kb_generator import generate_kb
from parser import read_input
from utils import format_output, save_board


SOLVERS = {
    "astar": solve_astar,
    "backtrack": solve_backtracking,
    "backward": solve_backward_chaining,
    "bruteforce": solve_bruteforce,
    "forward": solve_forward_chaining,
}


def default_output_path(input_path: str) -> str:
    base = os.path.basename(input_path).replace("input", "output")
    return os.path.join("Outputs", base)


def main() -> int:
    parser = argparse.ArgumentParser(description="Solve Futoshiki puzzles for AI Project 2.")
    parser.add_argument("input", nargs="?", default=os.path.join("Inputs", "input-01.txt"))
    parser.add_argument("--method", choices=sorted(SOLVERS), default="backtrack")
    parser.add_argument("--output", default=None)
    parser.add_argument("--show-kb", action="store_true", help="Print generated KB/CNF sizes.")
    args = parser.parse_args()

    N, grid, h_cons, v_cons = read_input(args.input)
    output_path = args.output or default_output_path(args.input)

    print(f"Solving {args.input} ({N}x{N}) with {args.method}...")
    start = time.perf_counter()
    solution = SOLVERS[args.method](N, grid, h_cons, v_cons)
    elapsed = time.perf_counter() - start

    if args.show_kb:
        kb = generate_kb(N, grid, h_cons, v_cons)
        cnf = generate_cnf(N, grid, h_cons, v_cons)
        facts = infer_facts(N, grid, h_cons, v_cons)
        print(f"KB facts: {len(kb['facts'])}; domain atoms: {len(kb['domains'])}; rules: {len(kb['rules'])}")
        print(f"CNF clauses: {len(cnf)}; inferred facts after propagation: {len(facts)}")

    if solution is None:
        print("No solution found.")
        return 1

    print(f"Solution found in {elapsed:.4f}s")
    print()
    print(format_output(N, solution, h_cons, v_cons))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    save_board(output_path, solution, h_cons, v_cons)
    print()
    print(f"Saved output to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
