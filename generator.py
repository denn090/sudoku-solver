import random
import copy
import datetime
import uuid
from solver import count_solutions

SIZES = {
    4: {'symbols': [str(i+1) for i in range(4)]},
    9: {'symbols': [str(i+1) for i in range(9)]},
    16: {'symbols': [str(i+1) for i in range(9)] + list("ABCDEFG")},
}

def generate(size, difficulty_level):
    difficulty_names = {0: "easy", 1: "medium", 2: "hard", 3: "expert"}
    if difficulty_level not in difficulty_names:
        raise ValueError("Schwierigkeitsgrad muss zwischen 0 und 3 liegen.")

    difficulty_str = difficulty_names[difficulty_level]
    holes_map = {0: int(size*size*0.4), 1: int(size*size*0.5), 2: int(size*size*0.6), 3: int(size*size*0.7)}
    holes = holes_map[difficulty_level]
    
    symbols = SIZES[size]['symbols']
    board = [['' for _ in range(size)] for _ in range(size)]
    fill_board(board, symbols)
    solution = copy.deepcopy(board)
    puzzle = copy.deepcopy(board)
    remove_cells(puzzle, holes, symbols)

    return {
        "id": str(uuid.uuid4()),
        "difficulty": difficulty_str,
        "board": puzzle,
        "solution": solution,
        "createdAt": datetime.datetime.utcnow().isoformat() + "Z"
    }

def fill_board(board, symbols):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == '':
                random.shuffle(symbols)
                for val in symbols:
                    if is_safe(board, i, j, val):
                        board[i][j] = val
                        if fill_board(board, symbols):
                            return True
                        board[i][j] = ''
                return False
    return True

def is_safe(board, row, col, val):
    from solver import valid
    return valid(board, row, col, val)

def remove_cells(board, holes, symbols):
    size = len(board)
    attempts = holes + 10
    while holes > 0 and attempts > 0:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if board[row][col] == '':
            continue
        backup = board[row][col]
        board[row][col] = ''
        test_board = copy.deepcopy(board)
        if count_solutions(test_board, symbols) == 1:
            holes -= 1
        else:
            board[row][col] = backup
        attempts -= 1
