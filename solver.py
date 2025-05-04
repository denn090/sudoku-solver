attempts = 0 

def valid(grid, row, col, num):
    if any(grid[row][i] == num for i in range(9)):
        return False
    if any(grid[i][col] == num for i in range(9)):
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

def solve(grid):
    global attempts
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for num in range(1, 10):
                    if valid(grid, i, j, num):
                        attempts += 1
                        grid[i][j] = num
                        if solve(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True

def solve_step_by_step(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for num in range(1, 10):
                    if valid(grid, i, j, num):
                        grid[i][j] = num
                        yield (i, j, num)
                        if not any(0 in row for row in grid):
                            yield None  
                        else:
                            yield from solve_step_by_step(grid)
                        grid[i][j] = 0
                return


def get_attempts():
    return attempts

def reset_attempts():
    global attempts
    attempts = 0

def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) for num in row))

if __name__ == '__main__':
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    reset_attempts()
    if solve(puzzle):
        print_grid(puzzle)
        print(f"Versuche: {get_attempts()}")
    else:
        print("Keine Lösung gefunden.")