# Futoshiki Lab 2

Python implementation for CSC14003 Project 2: Logic - Futoshiki Puzzles.

## Run

Run commands from this `Source` folder:

```bash
python main.py Inputs/input-01.txt --method backtrack --output Outputs/output-01.txt
```

Available methods:

- `backtrack`: MRV backtracking baseline
- `bruteforce`: exhaustive baseline, intended for small cases only
- `astar`: A* over partial assignments with the admissible remaining-cells heuristic
- `forward`: forward-chaining style constraint propagation with search when propagation stalls
- `backward`: SLD-style backward value queries with DFS search

Print KB/CNF statistics while solving:

```bash
python main.py Inputs/input-01.txt --method forward --show-kb --stats
```

Run the full experiment table:

```bash
python run_experiments.py
```

Open the optional GUI:

```bash
python gui.py
```

## Input Format

Each input follows the PDF specification:

```text
N
N grid rows, each with N comma-separated integers
N horizontal-constraint rows, each with N-1 comma-separated integers
N-1 vertical-constraint rows, each with N comma-separated integers
```

Grid values:

- `0`: empty cell
- `1..N`: given clue

Constraint values:

- `0`: no inequality
- `1`: less-than (`left < right` or `top < bottom`)
- `-1`: greater-than (`left > right` or `top > bottom`)

The parser ignores blank lines and text after `#`, so comments are allowed.

## Files

- `Inputs/input-01.txt` ... `Inputs/input-10.txt`: required test cases across 4x4, 5x5, 6x6, 7x7, and 9x9.
- `Outputs/output-XX.txt`: generated solved grids.
- `Outputs/experiment_results.csv`: generated runtime/memory/inference comparison table.
- `gui.py`: optional Tkinter GUI for bonus demonstration.
- `demo_script.md`: suggested recording script for the required demonstration videos.
- `kb_generator.py`: finite ground KB facts/rules.
- `cnf_generator.py`: propositional CNF clauses for Futoshiki constraints.
- `forward_chaining.py`, `backward_chaining.py`, `astar.py`, `backtracking.py`: solving algorithms.
