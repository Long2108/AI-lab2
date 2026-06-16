# Futoshiki Lab2 Starter

This workspace contains a starter implementation for the Futoshiki lab.

Run the solver from the repository root using the Source package:

```bash
python -m Source.main Source/Inputs/input-01.txt --method backtrack --output Source/Outputs/output-01.txt
```

Input format (`inputs/*.txt`):
- First line: N
- Next N lines: N tokens each (numbers or `.` for empty)
- Optional constraint lines: `H i j <` or `V i j >` (1-based indices)

Files added:
- `Lab2_Requirements.md`: assignment specification
# `StudentID1_StudentID2/Source/futoshiki.py`: Puzzle and Solver implementations
# `StudentID1_StudentID2/Source/main.py`: CLI runner
# `StudentID1_StudentID2/Source/Inputs/input-01.txt`: sample input
# AI-lab2