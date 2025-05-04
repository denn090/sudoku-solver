def count_empty(grid):
    return sum(row.count(0) for row in grid)

def estimate_difficulty(empty: int, attempts: int) -> str:
    score = empty + 0.01 * attempts

    if score < 55:
        return "Leicht"
    elif score < 65:
        return "Mittel"
    else:
        return "Schwer"