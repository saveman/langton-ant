from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


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
        self.__d = Direction.NORTH
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
        if self.__d == Direction.NORTH:
            self.__d = Direction.EAST
        elif self.__d == Direction.EAST:
            self.__d = Direction.SOUTH
        elif self.__d == Direction.SOUTH:
            self.__d = Direction.WEST
        else:
            self.__d = Direction.NORTH

    def __rotate_left(self):
        if self.__d == Direction.NORTH:
            self.__d = Direction.WEST
        elif self.__d == Direction.WEST:
            self.__d = Direction.SOUTH
        elif self.__d == Direction.SOUTH:
            self.__d = Direction.EAST
        else:
            self.__d = Direction.NORTH

    def __move(self):
        if self.__d == Direction.NORTH:
            self.__y -= 1
        elif self.__d == Direction.WEST:
            self.__x += 1
        elif self.__d == Direction.SOUTH:
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
