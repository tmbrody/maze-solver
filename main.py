from tkinter import Tk, BOTH, Canvas
from time import sleep

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=self.__width, height=self.__height)
        self.__canvas.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

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
        
class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()
        self._animate()
        self._break_entrance_and_exit()

    def _create_cells(self):
        for i in range(self._num_cols):
            column = []
            for j in range(self._num_rows):
                x1 = self._x1 + i * self._cell_size_x
                y1 = self._y1 + j * self._cell_size_y
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
                sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(0, 0)

        exit_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

def main():
    win = Window(800, 600)

    Maze(100, 100, 5, 5, 40, 40, win)

    win.wait_for_close()

if __name__ == "__main__":
    main()
