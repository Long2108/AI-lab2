# AI Lab 2 - Futoshiki

Implementation for Project 2: Logic - Futoshiki Puzzles.

Run from `Source`:

```bash
cd Source
python main.py Inputs/input-01.txt --method backtrack --output Outputs/output-01.txt
```

Methods: `backtrack`, `bruteforce`, `astar`, `forward`, `backward`.

Useful extras:

```bash
python main.py Inputs/input-01.txt --method forward --show-kb --stats
python run_experiments.py
python generate_report.py
python gui.py
```

Input files follow the assignment PDF CSV format:

- first line: `N`
- next `N` lines: grid values, comma-separated
- next `N` lines: horizontal constraints with `N-1` values
- next `N-1` lines: vertical constraints with `N` values

Use `0` for empty cells/no constraint, `1` for `<`, and `-1` for `>`.

Generated artifacts live in `Source/Outputs/` and `Source/Report.pdf`.
