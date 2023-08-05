import tkinter as tk
from tkinter import BOTH, Canvas, simpledialog
from time import sleep
import random
from collections import deque

class Window:
    def __init__(self, width=800, height=600):
        self.__width = width
        self.__height = height
        self.__root = tk.Tk()
        self.__root.title("Maze Solver")

        restart_button = tk.Button(self.__root, text="Restart", width=5, height=2, command=self.create_new_maze)
        restart_button.pack(side=tk.TOP, anchor=tk.NE)

        self.__canvas = Canvas(self.__root, width=self.__width, height=self.__height)
        self.__canvas.pack()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def get_maze_parameters(self):
        self.__root.withdraw()

        dialog = MazeParametersDialog(self.__root)
        self.__root.wait_window(dialog)

        y_pad = dialog.y_pad_var.get()
        num_rows = dialog.num_rows_var.get()
        num_cols = dialog.num_cols_var.get()
        cell_size_x = dialog.cell_size_x_var.get()
        cell_size_y = dialog.cell_size_y_var.get()

        self.__root.deiconify()

        return y_pad, num_rows, num_cols, cell_size_x, cell_size_y
    
    def resize_canvas(self, width, height):
        self.__width = width
        self.__height = height
        self.__canvas.config(width=width, height=height)
        self.__root.geometry(f"{width}x{height}")
    
    def create_new_maze(self):
        self.clear_canvas()
        y_pad, num_rows, num_cols, cell_size_x, cell_size_y = self.get_maze_parameters()
        maze_width = num_cols * cell_size_x
        window_width = maze_width * 2
        window_height = (num_rows * cell_size_y) * 2
        x_pad = (window_width - maze_width) // 2
        self.resize_canvas(window_width, window_height)
        
        while True:
            maze = Maze(x_pad, y_pad, num_rows, num_cols, cell_size_x, cell_size_y, self)
            maze.generate_maze()
            maze.solve()
            sleep(0.5)
            self.clear_canvas()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def clear_canvas(self):
        self.__canvas.delete("all")

    def close(self):
        self.__root.destroy()

class MazeParametersDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x300")
        self.title("Maze Parameters")
        self.parent = parent

        self.y_pad_var = tk.IntVar(value=20)
        self.num_rows_var = tk.IntVar(value=20)
        self.num_cols_var = tk.IntVar(value=20)
        self.cell_size_x_var = tk.IntVar(value=20)
        self.cell_size_y_var = tk.IntVar(value=20)

        self.protocol("WM_DELETE_WINDOW", self.master.destroy)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter the maze parameters:").pack()

        tk.Label(self, text="Maze top padding:").pack()
        tk.Entry(self, textvariable=self.y_pad_var).pack()

        tk.Label(self, text="Number of rows:").pack()
        tk.Entry(self, textvariable=self.num_rows_var).pack()

        tk.Label(self, text="Number of columns:").pack()
        tk.Entry(self, textvariable=self.num_cols_var).pack()

        tk.Label(self, text="Cell Width:").pack()
        tk.Entry(self, textvariable=self.cell_size_x_var).pack()

        tk.Label(self, text="Cell Height:").pack()
        tk.Entry(self, textvariable=self.cell_size_y_var).pack()

        tk.Button(self, text="OK", command=self.destroy).pack()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2
        )
        canvas.pack()

class Cell:
    def __init__(
            self, 
            x1, 
            y1, 
            x2, 
            y2, 
            has_left_wall=True, 
            has_right_wall=True, 
            has_top_wall=True, 
            has_bottom_wall=True
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = None
        self.visited = False

    def set_window(self, win=None):
        self._win = win

    def draw(self):
        wall_color = "black"
        background_color = "SystemButtonFace"

        if self.has_left_wall:
            self.draw_left(wall_color)
        else:
            self.draw_left(background_color)

        if self.has_right_wall:
            self.draw_right(wall_color)
        else:
            self.draw_right(background_color)

        if self.has_top_wall:
            self.draw_top(wall_color)
        else:
            self.draw_top(background_color)

        if self.has_bottom_wall:
            self.draw_bottom(wall_color)
        else:
            self.draw_bottom(background_color)

    def draw_left(self, color):
        self._win.draw_line(Line(
                self._x1, self._y1, self._x1, self._y2), color
            )
        
    def draw_right(self, color):
        self._win.draw_line(Line(
                self._x2, self._y1, self._x2, self._y2), color
            )
        
    def draw_top(self, color):
        self._win.draw_line(Line(
                self._x1, self._y1, self._x2, self._y1), color
            )

    def draw_bottom(self, color):
        self._win.draw_line(Line(
                self._x1, self._y2, self._x2, self._y2), color
            )

    def draw_move(self, to_cell, undo=False):
        x1_center = (self._x1 + self._x2) // 2
        y1_center = (self._y1 + self._y2) // 2
        x2_center = (to_cell._x1 + to_cell._x2) // 2
        y2_center = (to_cell._y1 + to_cell._y2) // 2

        line_color = "gray" if undo else "red"

        self._win.draw_line(Line(
            x1_center, y1_center, x2_center, y2_center), line_color)
        
    def has_wall_to(self, other_cell):
        if self._x2 == other_cell._x1:
            return self.has_right_wall or other_cell.has_left_wall
        elif self._x1 == other_cell._x2:
            return self.has_left_wall or other_cell.has_right_wall
        elif self._y2 == other_cell._y1:
            return self.has_bottom_wall or other_cell.has_top_wall
        elif self._y1 == other_cell._y2:
            return self.has_top_wall or other_cell.has_bottom_wall
        return False
        
class Maze:
    def __init__(
            self,
            x_pad,
            y_pad,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None,
    ):
        self._x_pad = x_pad
        self._y_pad = y_pad
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

        self._cells = []
        self._create_cells()
        self._animate()
        self._break_entrance_and_exit()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                x1 = self._x_pad + i * self._cell_size_x
                y1 = self._y_pad + j * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                cell = Cell(x1, y1, x2, y2)
                cell.set_window(self._win)
                column.append(cell)
            self._cells.append(column)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()

    def _animate(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
                self._win.redraw()

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(0, 0)

        exit_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        queue = deque([(i, j)])
        self._cells[i][j].visited = True

        while queue:
            i, j = queue.popleft()
            current_cell = self._cells[i][j]
            current_cell.visited = True
            possible_directions = []

            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append((i, j - 1))

            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append((i + 1, j))

            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                possible_directions.append((i, j + 1))

            if i > 0 and not self._cells[i - 1][j].visited:
                possible_directions.append((i - 1, j))

            if not possible_directions:
                self._draw_cell(i, j)
            else:
                i_next, j_next = random.choice(possible_directions)
                next_cell = self._cells[i_next][j_next]

                if i_next > i:
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                elif i_next < i:
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
                elif j_next > j:
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False
                elif j_next < j:
                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False

                self._draw_cell(i, j)
                queue.append((i_next, j_next))
                next_cell.visited = True
                self._break_walls_r(i_next, j_next)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def generate_maze(self):
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._win.redraw()
        sleep(0.01)

        current_cell = self._cells[i][j]
        current_cell.visited = True

        if current_cell == self._cells[self._num_cols - 1][self._num_rows - 1]:
            return True
        
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            next_i, next_j = i + dx, j + dy
            if 0 <= next_i < self._num_cols and 0 <= next_j < self._num_rows:
                next_cell = self._cells[next_i][next_j]
                if not current_cell.has_wall_to(next_cell) and not next_cell.visited:
                    current_cell.draw_move(next_cell)
                    if self._solve_r(next_i, next_j):
                        return True
                    next_cell.draw_move(current_cell, True)
        return False

def main():
    win = Window()
    win.create_new_maze()
    
if __name__ == "__main__":
    main()
