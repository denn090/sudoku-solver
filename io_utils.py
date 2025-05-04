import json
import os


def validate_sudoku_data(data):
    # Überprüfe, ob alle notwendigen Felder vorhanden sind.
    if "id" not in data or "board" not in data or "solution" not in data:
        raise ValueError("JSON muss 'id', 'board' und 'solution' enthalten.")

    # Validierung des Boards: 9x9-Gitter, Werte zwischen 0 und 9 (0 = leeres Feld).
    board = data["board"]
    if not isinstance(board, list) or len(board) != 9:
        raise ValueError("'board' muss eine Liste mit 9 Zeilen sein.")
    for row in board:
        if not isinstance(row, list) or len(row) != 9:
            raise ValueError("Jede Zeile in 'board' muss 9 Einträge haben.")
        for value in row:
            if not isinstance(value, int) or not (0 <= value <= 9):
                raise ValueError("Werte in 'board' müssen Ganzzahlen zwischen 0 und 9 sein.")

    # Validierung der Lösung: darf None sein, ansonsten 9x9-Gitter mit Werten zwischen 1 und 9.
    solution = data["solution"]
    if solution is not None:
        if not isinstance(solution, list) or len(solution) != 9:
            raise ValueError("'solution' muss None oder eine Liste mit 9 Zeilen sein.")
        for row in solution:
            if not isinstance(row, list) or len(row) != 9:
                raise ValueError("Jede Zeile in 'solution' muss 9 Einträge haben.")
            for value in row:
                if not isinstance(value, int) or not (1 <= value <= 9):
                    raise ValueError("Werte in 'solution' müssen Ganzzahlen zwischen 1 und 9 sein.")


def import_sudoku(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validierung
    validate_sudoku_data(data)

    return data.get("board")


def export_sudoku(filepath, sudoku_data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sudoku_data, f, indent=2, ensure_ascii=False)
