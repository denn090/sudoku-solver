def valid(grid, row, col, val):
    size = len(grid)
    block = int(size ** 0.5)
    if val in grid[row]:
        return False
    if val in [grid[i][col] for i in range(size)]:
        return False
    start_row, start_col = (row // block) * block, (col // block) * block
    for i in range(start_row, start_row + block):
        for j in range(start_col, start_col + block):
            if grid[i][j] == val:
                return False
    return True

def solve(grid, symbols):
    size = len(grid)
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '':
                for val in symbols:
                    if valid(grid, i, j, val):
                        grid[i][j] = val
                        if solve(grid, symbols):
                            return True
                        grid[i][j] = ''
                return False
    return True

def count_solutions(grid, symbols):
    count = 0
    size = len(grid)

    def backtrack():
        nonlocal count
        for i in range(size):
            for j in range(size):
                if grid[i][j] == '':
                    for val in symbols:
                        if valid(grid, i, j, val):
                            grid[i][j] = val
                            backtrack()
                            grid[i][j] = ''
                    return
        count += 1
        if count > 1:
            return

    backtrack()
    return count

def solve_step_by_step(grid, symbols):
    size = len(grid)
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '':
                for val in symbols:
                    if valid(grid, i, j, val):
                        grid[i][j] = val
                        yield (i, j, val)
                        yield from solve_step_by_step(grid, symbols)
                        grid[i][j] = ''
                return
    yield None

_attempts = 0 

def reset_attempts():
    global _attempts
    _attempts = 0

def get_attempts():
    return _attempts