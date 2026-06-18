"""Run all solvers on all required inputs and export comparison tables."""

import csv
import os
import time
import tracemalloc
from pathlib import Path

from astar import solve_astar_result
from backtracking import solve_backtracking_result, solve_bruteforce_result
from backward_chaining import solve_backward_chaining_result
from forward_chaining import solve_forward_chaining_result
from parser import read_input


SOLVERS = {
    "bruteforce": solve_bruteforce_result,
    "backtrack": solve_backtracking_result,
    "forward": solve_forward_chaining_result,
    "backward": solve_backward_chaining_result,
    "astar": solve_astar_result,
}


def run_case(method, solver, input_path):
    N, grid, h_cons, v_cons = read_input(str(input_path))
    tracemalloc.start()
    start = time.perf_counter()
    result = solver(N, grid, h_cons, v_cons)
    runtime = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    stats = result.stats
    stats.runtime = runtime
    return {
        "input": input_path.name,
        "N": N,
        "method": method,
        "solved": result.grid is not None,
        "runtime_seconds": f"{runtime:.6f}",
        "peak_kb": f"{peak / 1024:.1f}",
        "nodes_expanded": stats.nodes_expanded,
        "assignments_tried": stats.assignments_tried,
        "inferences": stats.inferences,
        "contradictions": stats.contradictions,
        "max_frontier": stats.max_frontier,
    }


def write_markdown(rows, path):
    headers = [
        "input",
        "N",
        "method",
        "solved",
        "runtime_seconds",
        "peak_kb",
        "nodes_expanded",
        "assignments_tried",
        "inferences",
        "contradictions",
        "max_frontier",
    ]
    lines = ["# Experiment Results", "", "| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    base = Path(__file__).resolve().parent
    inputs = sorted((base / "Inputs").glob("input-*.txt"))
    out_dir = base / "Outputs"
    out_dir.mkdir(exist_ok=True)

    rows = []
    for input_path in inputs:
        for method, solver in SOLVERS.items():
            row = run_case(method, solver, input_path)
            rows.append(row)
            print(
                f"{row['input']} {method}: solved={row['solved']} "
                f"time={row['runtime_seconds']}s nodes={row['nodes_expanded']}"
            )

    csv_path = out_dir / "experiment_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    write_markdown(rows, out_dir / "experiment_results.md")
    print(f"Wrote {os.path.relpath(csv_path, base)}")


if __name__ == "__main__":
    main()

