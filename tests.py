import unittest
from unittest.mock import MagicMock
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 15
        num_rows = 12
        win = MagicMock()
        maze = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(maze._cells),
            num_cols
        )
        self.assertEqual(
            len(maze._cells[0]),
            num_rows
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 3
        num_rows = 3
        win = MagicMock()
        maze = Maze(0, 0, num_rows, num_cols, 20, 20, win)

        entrance_cell = maze._cells[0][0]
        exit_cell = maze._cells[num_cols - 1][num_rows - 1]

        maze._break_entrance_and_exit()

        self.assertFalse(entrance_cell.has_top_wall)
        self.assertTrue(entrance_cell.has_bottom_wall)
        self.assertTrue(entrance_cell.has_left_wall)
        self.assertTrue(entrance_cell.has_right_wall)

        self.assertFalse(exit_cell.has_bottom_wall)
        self.assertTrue(exit_cell.has_top_wall)
        self.assertTrue(exit_cell.has_left_wall)
        self.assertTrue(exit_cell.has_right_wall)

if __name__ == "__main__":
    unittest.main()
