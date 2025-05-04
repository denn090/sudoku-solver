import pytest
import tempfile
import json
import os
from sudoku_solver.io_utils import import_sudoku  # Passe den Import je nach Projektstruktur an.


# Hilfsfunktion zum Schreiben temporärer JSON-Dateien
def write_temp_json(data):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8')
    json.dump(data, tmp)
    tmp.close()
    return tmp.name


def test_valid_sudoku_with_solution():
    sudoku = {
        "id": "test_001",
        "board": [[0] * 9 for _ in range(9)],
        "solution": [[i % 9 + 1 for i in range(9)] for _ in range(9)]
    }
    path = write_temp_json(sudoku)
    result = import_sudoku(path)
    assert result["id"] == "test_001"
    os.remove(path)


def test_valid_sudoku_without_solution():
    sudoku = {
        "id": "test_002",
        "board": [[0] * 9 for _ in range(9)],
        "solution": None
    }
    path = write_temp_json(sudoku)
    result = import_sudoku(path)
    assert result["solution"] is None
    os.remove(path)


def test_missing_fields():
    sudoku = {
        "id": "test_003",
        "board": [[0] * 9 for _ in range(9)]
        # Feld "solution" fehlt absichtlich
    }
    path = write_temp_json(sudoku)
    with pytest.raises(ValueError, match="JSON muss 'id', 'board' und 'solution' enthalten"):
        import_sudoku(path)
    os.remove(path)


def test_invalid_board_size():
    sudoku = {
        "id": "test_004",
        "board": [[0] * 9 for _ in range(8)],  # zu wenige Zeilen
        "solution": None
    }
    path = write_temp_json(sudoku)
    with pytest.raises(ValueError, match="'board' muss eine Liste mit 9 Zeilen sein"):
        import_sudoku(path)
    os.remove(path)


def test_invalid_board_value():
    sudoku = {
        "id": "test_005",
        "board": [[0] * 9 for _ in range(9)],
        "solution": [[10] * 9 for _ in range(9)]  # ungültige Werte in der Lösung (10 statt 1-9)
    }
    path = write_temp_json(sudoku)
    with pytest.raises(ValueError, match="Werte in 'solution' müssen Ganzzahlen zwischen 1 und 9 sein."):
        import_sudoku(path)
    os.remove(path)
