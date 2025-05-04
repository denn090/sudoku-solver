import tkinter as tk
from tkinter import messagebox
from solver import solve

class SudokuGUI:
    def __init__(self, master, init_grid=None):
        self.master = master
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()
        if init_grid is not None:
            self.set_grid(init_grid)

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0, padx=10, pady=10)
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(frame, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry

        btn_solve = tk.Button(self.master, text="Solve", command=self.solve_sudoku)
        btn_solve.grid(row=1, column=0, pady=(10,0))
        btn_clear = tk.Button(self.master, text="Clear", command=self.clear_grid)
        btn_clear.grid(row=2, column=0, pady=(5,0))

    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            grid.append(row)
        return grid

    def set_grid(self, grid):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(grid[i][j]))

    def solve_sudoku(self):
        grid = self.get_grid()
        if solve(grid):
            self.set_grid(grid)
        else:
            messagebox.showinfo("Sudoku", "Keine Lösung gefunden!")

    def clear_grid(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)

def run_gui(init_grid=None):
    root = tk.Tk()
    root.title("Sudoku Solver GUI")
    SudokuGUI(root, init_grid)
    root.mainloop()