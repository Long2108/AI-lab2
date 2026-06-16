from parser import read_input
from backtracking import solve_backtracking
from typing import List, Tuple

def format_output(N: int, grid: List[List[int]], h_cons: List[List[int]], v_cons: List[List[int]]) -> str:
    """
    Format solved grid with inequality symbols for output.
    
    Format:
    num [< or >] num [< or >] num ...
    [^ or v] [^ or v] ...
    num [< or >] num ...
    ...
    """
    lines = []
    
    for row_idx in range(N):
        # Build horizontal line for this row
        row_line = ""
        for col_idx in range(N):
            row_line += str(grid[row_idx][col_idx])
            
            # Add horizontal constraint between this and next cell
            if col_idx < N - 1:
                h_constraint = h_cons[row_idx][col_idx]
                if h_constraint == 1:
                    row_line += " < "
                elif h_constraint == -1:
                    row_line += " > "
                else:
                    row_line += "   "  # 3 spaces for empty constraint
        
        lines.append(row_line)
        
        # Vertical constraints after this row (if not last row)
        if row_idx < N - 1:
            v_line = ""
            for col_idx in range(N):
                v_constraint = v_cons[row_idx][col_idx]
                if v_constraint == 1:
                    v_line += "^"
                elif v_constraint == -1:
                    v_line += "v"
                else:
                    v_line += " "
                
                # Add spacing between constraint symbols
                if col_idx < N - 1:
                    v_line += " "
            
            lines.append(v_line)
    
    return '\n'.join(lines)


def save_output(N: int, grid: List[List[int]], h_cons: List[List[int]], v_cons: List[List[int]], output_path: str):
    """Save formatted solution to file."""
    output = format_output(N, grid, h_cons, v_cons)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)


# Main execution
N, grid, h_cons, v_cons = read_input("Inputs/input-01.txt")

print("Solving Futoshiki puzzle...")
print(f"Grid size: {N}x{N}")

# Solve using backtracking
solution = solve_backtracking(N, grid, h_cons, v_cons)

if solution:
    print("✓ Solution found!")
    print("\nSolved grid:")
    print(format_output(N, solution, h_cons, v_cons))
    
    # Save to output file
    save_output(N, solution, h_cons, v_cons, "Outputs/output-01.txt")
    print("\n✓ Output saved to Outputs/output-01.txt")
else:
    print("✗ No solution found!")