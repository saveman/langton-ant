from tkinter import *
from tkinter.ttk import *

from langtonant.ant import Engine


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
