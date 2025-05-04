import unittest
import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gui_main import SudokuGUI

class TestSudokuGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Fenster verstecken, damit es nicht angezeigt wird
        self.gui = SudokuGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_set_grid(self):
        # Beispiel-Gitter, das in die GUI geladen wird
        grid = [
            [1,2,3,4,5,6,7,8,9],
            [9,8,7,6,5,4,3,2,1],
            [1,2,3,4,5,6,7,8,9],
            [9,8,7,6,5,4,3,2,1],
            [1,2,3,4,5,6,7,8,9],
            [9,8,7,6,5,4,3,2,1],
            [1,2,3,4,5,6,7,8,9],
            [9,8,7,6,5,4,3,2,1],
            [1,2,3,4,5,6,7,8,9],
        ]
        self.gui.set_grid(grid)
        # Test: Erstes Feld muss "1" anzeigen
        self.assertEqual(self.gui.entries[0][0].get(), "1")
        # Test: Letztes Feld (in der 2. Zeile) muss "1" anzeigen
        self.assertEqual(self.gui.entries[1][8].get(), "1")

    def test_get_grid(self):
        # Simuliere Eingaben: Fülle ein paar Felder manuell
        self.gui.entries[0][0].insert(0, "8")
        self.gui.entries[0][1].insert(0, "5")
        grid = self.gui.get_grid()
        self.assertEqual(grid[0][0], 8)
        self.assertEqual(grid[0][1], 5)
        # Felder ohne Eingabe sollen 0 ergeben
        self.assertEqual(grid[0][2], 0)

if __name__ == '__main__':
    unittest.main()
