import tkinter as tk
from tkinter import messagebox
from generator import generate
from solver import solve

SIZES = {
    4: {'block_size': 2, 'symbols': [str(i+1) for i in range(4)]},
    9: {'block_size': 3, 'symbols': [str(i+1) for i in range(9)]},
    16: {'block_size': 4, 'symbols': [str(i+1) for i in range(9)] + list("ABCDEFG")},
}

class SudokuGUI:
    def __init__(self, master, size, difficulty, custom_input=False):
        self.master = master
        self.size = size
        self.block = SIZES[size]['block_size']
        self.symbols = SIZES[size]['symbols']
        self.entries = [[None for _ in range(size)] for _ in range(size)]
        self.difficulty = difficulty
        self.custom_input = custom_input
        self.create_widgets()
        if not self.custom_input:
            self.new_game()

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0, padx=10, pady=10)
        for i in range(self.size):
            for j in range(self.size):
                entry = tk.Entry(frame, width=2 if self.size > 9 else 3, font=('Arial', 16), justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                self.entries[i][j] = entry

        btn_frame = tk.Frame(self.master)
        btn_frame.grid(row=1, column=0, pady=(10, 0))

        tk.Button(btn_frame, text="Zurück zur Auswahl", command=self.back_to_launcher).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Lösen", command=self.solve_sudoku).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Leeren", command=self.clear_grid).pack(side=tk.LEFT, padx=5)

    def new_game(self):
        data = generate(self.size, self.difficulty)
        self.set_grid(data["board"])

    def back_to_launcher(self):
        self.master.destroy()
        from gui_main import launcher
        launcher()

    def get_grid(self):
        grid = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                val = self.entries[i][j].get().upper()
                row.append(val if val in self.symbols else '')
            grid.append(row)
        return grid

    def set_grid(self, grid):
        for i in range(self.size):
            for j in range(self.size):
                self.entries[i][j].delete(0, tk.END)
                if grid[i][j] != '':
                    self.entries[i][j].insert(0, str(grid[i][j]))

    def solve_sudoku(self):
        grid = self.get_grid()
        if solve(grid, self.symbols):
            self.set_grid(grid)
        else:
            messagebox.showinfo("Sudoku", "Keine Lösung gefunden!")

    def clear_grid(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)


def launcher():
    root = tk.Tk()
    root.title("Sudoku Launcher")

    tk.Label(root, text="Größe wählen:").pack()
    size_var = tk.IntVar(value=9)
    tk.OptionMenu(root, size_var, *SIZES.keys()).pack()

    diff_var = tk.IntVar(value=0)
    difficulty_menu = tk.Frame(root)
    difficulty_menu.pack()

    difficulty_menus = {
        4: [("Einfach", 0), ("Mittel", 1), ("Schwer", 2), ("Experte", 3)],
        9: [("Einfach", 0), ("Mittel", 1), ("Schwer", 2), ("Experte", 3)],
        16: [("Einfach", 0)]
    }

    def update_difficulties(*args):
        for widget in difficulty_menu.winfo_children():
            widget.destroy()
        current_size = size_var.get()
        options = difficulty_menus[current_size]
        menu_label = tk.Label(difficulty_menu, text="Schwierigkeit wählen:")
        menu_label.pack()
        menu_values = [v for _, v in options]
        tk.OptionMenu(difficulty_menu, diff_var, *menu_values).pack()

    size_var.trace_add('write', update_difficulties)
    update_difficulties()

    def start():
        root.destroy()
        win = tk.Tk()
        win.title("Sudoku GUI")
        SudokuGUI(win, size_var.get(), diff_var.get())
        win.mainloop()

    def start_custom():
        root.destroy()
        win = tk.Tk()
        win.title("Eigenes Sudoku")
        SudokuGUI(win, size_var.get(), diff_var.get(), custom_input=True)
        win.mainloop()

    tk.Button(root, text="Start", command=start).pack(pady=5)
    tk.Button(root, text="Eigenes Sudoku eingeben", command=start_custom).pack(pady=5)

    root.mainloop()