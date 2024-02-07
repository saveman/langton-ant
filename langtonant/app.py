import copy
from tkinter import *
from tkinter.ttk import *


class Board:
    def __init__(self, width: int, height: int) -> None:
        self.__width = width
        self.__height = height
        self.__data = [[0 for _ in range(self.__width)] for _ in range(self.__height)]

    def width(self) -> int:
        return self.__width

    def heigth(self) -> int:
        return self.__height

    def get(self, x: int, y: int) -> int:
        return self.__data[x][y]

    def set(self, x: int, y: int, value: int) -> None:
        self.__data[x][y] = value


class Engine:
    BOARD_WIDTH = 200
    BOARD_HEIGHT = 200

    def __init__(self):
        self.__x = self.BOARD_WIDTH // 2
        self.__y = self.BOARD_HEIGHT // 2
        self.__d = N
        self.__board = Board(self.BOARD_WIDTH, self.BOARD_HEIGHT)

    def get_board(self):
        # return copy.deepcopy(self.__board)
        return self.__board

    def execute_step(self):
        print(f'Execute x={self.__x} y={self.__y} d={self.__d}')

        val = self.__board.get(self.__x, self.__y)

        if val:
            self.__rotate_right()
            self.__board.set(self.__x, self.__y, 0)
        else:
            self.__rotate_left()
            self.__board.set(self.__x, self.__y, 1)

        self.__move()

    def __rotate_right(self):
        if self.__d == N:
            self.__d = E
        elif self.__d == E:
            self.__d = S
        elif self.__d == S:
            self.__d = W
        else:
            self.__d = N

    def __rotate_left(self):
        if self.__d == N:
            self.__d = W
        elif self.__d == W:
            self.__d = S
        elif self.__d == S:
            self.__d = E
        else:
            self.__d = N

    def __move(self):
        if self.__d == N:
            self.__y -= 1
        elif self.__d == W:
            self.__x += 1
        elif self.__d == S:
            self.__y += 1
        else:
            self.__x -= 1

        if self.__x < 0:
            self.__x = self.BOARD_WIDTH - 1
        if self.__x >= self.BOARD_WIDTH:
            self.__x = 0
        if self.__y < 0:
            self.__y = self.BOARD_HEIGHT - 1
        if self.__y >= self.BOARD_HEIGHT:
            self.__y = 0


class LangtonAntApp:
    REFRESH_TIME_MS = 100

    def __init__(self) -> None:
        self.__engine = Engine()

        self.__root = None
        self.__frame = None
        self.__image = None

    def __donothing(self):
        # filewin = Toplevel(root)
        # button = Button(filewin, text="Do nothing button")
        # button.pack()
        pass

    def run(self):
        self.__root = Tk()
        self.__root.title('Langton Ant')
        self.__root.rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=1)

        menubar = Menu(self.__root)
        self.__root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", underline=1, command=self.__on_exit)

        menubar.add_cascade(label="File", underline=0, menu=file_menu)

        self.__frame = Frame(self.__root, padding=10)
        self.__frame.grid(sticky=NSEW)
        self.__frame.columnconfigure([0], weight=1)
        self.__frame.rowconfigure([0], weight=1)

        canvas = Canvas(self.__frame, bg="#333333", relief='ridge', highlightthickness=0)
        canvas.grid(column=0, row=0, sticky="news")

        self.__image = self.__make_image()

        canvas.create_image((0, 0), image=self.__image, state="normal", anchor=NW)

        self.__schedule_refresh()

        self.__root.mainloop()

    def __make_image(self):
        board = self.__engine.get_board()

        image = PhotoImage(width=board.width(), height=board.heigth())
        for i in range(0, board.width()):
            image.put("#FF0000", to=(i, 0))
        for i in range(0, board.heigth()):
            image.put("#0000FF", to=(0, i))

        return image

    def __update_image(self):
        print('Update')

        board = self.__engine.get_board()

        width = board.width()
        height = board.heigth()

        t = (0, 0)

        for y in range(0, height):
            for x in range(0, width):
                val = board.get(x, y)
                if val:
                    self.__image.put('#000000', to=(x, y))
                else:
                    self.__image.put('#FFFFFF', to=(x, y))

        print('Update done')

    def __schedule_refresh(self):
        self.__frame.after(self.REFRESH_TIME_MS, self.__on_refresh)

    def __on_exit(self):
        self.__root.destroy()

    def __on_refresh(self):
        for i in range(0, 1000):
            self.__engine.execute_step()

        self.__update_image()

        self.__schedule_refresh()
