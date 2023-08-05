from tkinter import Tk, BOTH, Canvas

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
    def __init__(self, x1, y1, x2, y2, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = None

    def set_window(self, win):
        self._win = win

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(
                self._x1, self._y1, self._x1, self._y2), "black"
            )

        if self.has_right_wall:
            self._win.draw_line(Line(
                self._x2, self._y1, self._x2, self._y2), "black"
            )

        if self.has_top_wall:
            self._win.draw_line(Line(
                self._x1, self._y1, self._x2, self._y1), "black"
            )

        if self.has_bottom_wall:
            self._win.draw_line(Line(
                self._x1, self._y2, self._x2, self._y2), "black"
            )


def main():
    win = Window(800, 600)

    cell1 = Cell(300, 50, 400, 100)
    cell2 = Cell(500, 200, 600, 300, has_left_wall=False, has_right_wall=False)

    cell1.set_window(win)
    cell2.set_window(win)

    cell1.draw()
    cell2.draw()

    win.wait_for_close()

if __name__ == "__main__":
    main()
