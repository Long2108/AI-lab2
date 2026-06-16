## Project 2 — Logic: Futoshiki Puzzles

This file contains the lab2 requirements and specification for the Futoshiki project.

(Full original specification attached by the instructor follows.)

-- Copy of provided assignment --

Futoshiki Puzzles

1. Overview

Futoshiki (meaning "inequality" in Japanese) is a logic-based number placement puzzle played on an N × N grid. The player fills numbers 1..N obeying row/column permutations, inequality constraints, and given clues.

2. Puzzle Rules

- Each row is a permutation of 1..N.
- Each column is a permutation of 1..N.
- Inequality constraints (< or >) between adjacent cells must hold.
- Given clues are respected.

3. Formalization, inference methods, and implementation requirements

See the original PDF / assignment document provided to the course for detailed FOL axioms, grounding, CNF conversion, and required algorithms:

- Automatic KB grounding and CNF generation
- Forward chaining implementation
- Backward chaining (SLD) implementation
- A* search with an admissible heuristic
- Brute-force/backtracking baseline

4. Inputs and outputs

- Provide at least 10 input files (input-01.txt ... input-10.txt) across sizes 4x4, 5x5, 6x6, 7x7, 9x9.
- Output solved grids to stdout and to matching output files.

5. Implementation language

- Python 3.7+ required. Core algorithms (forward/backward/A*/backtracking) must be implemented from scratch.

-- End copy --

I created a small starter implementation in `src/` that implements a working backtracking solver and a simple A* search with a trivial admissible heuristic (remaining unassigned cells). Use the `README.md` for run instructions.
