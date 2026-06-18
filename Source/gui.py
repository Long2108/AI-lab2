"""Small Tkinter GUI for solving Futoshiki inputs."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from astar import solve_astar
from backtracking import solve_backtracking, solve_bruteforce
from backward_chaining import solve_backward_chaining
from forward_chaining import solve_forward_chaining
from parser import read_input
from utils import format_output


SOLVERS = {
    "backtrack": solve_backtracking,
    "bruteforce": solve_bruteforce,
    "astar": solve_astar,
    "forward": solve_forward_chaining,
    "backward": solve_backward_chaining,
}


class FutoshikiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Futoshiki Solver")
        self.geometry("780x560")
        self.input_path = tk.StringVar(value=str(Path("Inputs") / "input-01.txt"))
        self.method = tk.StringVar(value="backtrack")
        self._build()

    def _build(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Input").pack(side="left")
        ttk.Entry(top, textvariable=self.input_path, width=58).pack(side="left", padx=8, fill="x", expand=True)
        ttk.Button(top, text="Browse", command=self.browse).pack(side="left")

        controls = ttk.Frame(self, padding=(10, 0, 10, 10))
        controls.pack(fill="x")
        ttk.Label(controls, text="Method").pack(side="left")
        ttk.Combobox(controls, textvariable=self.method, values=sorted(SOLVERS), state="readonly", width=14).pack(side="left", padx=8)
        ttk.Button(controls, text="Solve", command=self.solve).pack(side="left")

        self.output = tk.Text(self, wrap="none", font=("Consolas", 12))
        self.output.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def browse(self):
        path = filedialog.askopenfilename(initialdir="Inputs", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            self.input_path.set(path)

    def solve(self):
        try:
            N, grid, h_cons, v_cons = read_input(self.input_path.get())
            solution = SOLVERS[self.method.get()](N, grid, h_cons, v_cons)
            if solution is None:
                messagebox.showwarning("No solution", "No solution found.")
                return
            self.output.delete("1.0", "end")
            self.output.insert("end", format_output(N, solution, h_cons, v_cons))
        except Exception as exc:
            messagebox.showerror("Error", str(exc))


if __name__ == "__main__":
    FutoshikiApp().mainloop()

