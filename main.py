from gui_main import run_gui
from io_utils import import_sudoku

def main():
    puzzle = import_sudoku("dva-gruppe-52/versuch-2/sudoku_solver/examples/001.json")
    run_gui(puzzle)

if __name__ == '__main__':
    main()
