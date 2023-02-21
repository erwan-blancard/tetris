import pygame

TILESIZE = 24

B_EMPTY = 0
B_CYAN = 1  # I
B_YELLOW = 2  # O
B_PURPLE = 3  # T
B_GREEN = 4  # S
B_RED = 5  # Z
B_BLUE = 6  # J
B_ORANGE = 7  # L

T_I = [
    [[False, False, False, False],
     [True, True, True, True],
     [False, False, False, False],
     [False, False, False, False]],

    [[False, False, True, False],
     [False, False, True, False],
     [False, False, True, False],
     [False, False, True, False]],

    [[False, False, False, False],
     [False, False, False, False],
     [True, True, True, True],
     [False, False, False, False]],

    [[False, True, False, False],
     [False, True, False, False],
     [False, True, False, False],
     [False, True, False, False]]
]

T_O = [
    [[True, True],
     [True, True]]
]
T_J = [
    [[True, False, False],
     [True, True, True],
     [False, False, False]],

    [[False, True, True],
     [False, True, False],
     [False, True, False]],

    [[False, False, False],
     [True, True, True],
     [False, False, True]],

    [[False, True, False],
     [False, True, False],
     [True, True, False]]

]
T_L = [
    [[False, False, True],
     [True, True, True],
     [False, False, False]],

    [[False, True, False],
     [False, True, False],
     [False, True, True]],

    [[False, False, False],
     [True, True, True],
     [True, False, False]],

    [[True, True, False],
     [False, True, False],
     [False, True, False]]
]
T_Z = [
    [[True, True, False],
     [False, True, True],
     [False, False, False]],

    [[False, False, True],
     [False, True, True],
     [False, True, False]],

    [[False, False, False],
     [True, True, False],
     [False, True, True]],

    [[False, True, False],
     [True, True, False],
     [True, False, False]]
]
T_T = [
    [[False, True, False],
     [True, True, True],
     [False, False, False]],

    [[False, True, False],
     [False, True, True],
     [False, True, False]],

    [[False, False, False],
     [True, True, True],
     [False, True, False]],

    [[False, True, False],
     [True, True, False],
     [False, True, False]]
]
T_S = [
    [[False, True, True],
     [True, True, False],
     [False, False, False]],

    [[False, True, False],
     [False, True, True],
     [False, False, True]],

    [[False, False, False],
     [False, True, True],
     [True, True, False]],

    [[True, False, False],
     [True, True, False],
     [False, True, False]]
]


def get_block_color(color_index):
    if color_index == B_CYAN:
        return 0, 255, 255
    elif color_index == B_YELLOW:
        return 255, 255, 0
    elif color_index == B_RED:
        return 255, 0, 0
    elif color_index == B_BLUE:
        return 0, 0, 255
    elif color_index == B_GREEN:
        return 0, 255, 0
    elif color_index == B_ORANGE:
        return 255, 128, 0
    elif color_index == B_PURPLE:
        return 128, 0, 255
    return 0, 0, 0


class TetrominoBase:

    def __init__(self, tiles: list[list[list[bool]]]):
        self.tiles = tiles
        self.current_tiles = 0
        self.color = -1

    # default expect 3x3
    def rotate(self, playfield: list[list[int]], pos: tuple[int, int], counter_clockwise=False):
        if not counter_clockwise:
            if self.current_tiles + 1 < 4:
                self.current_tiles += 1
            else:
                self.current_tiles = 0
        else:
            if self.current_tiles - 1 >= 0:
                self.current_tiles -= 1
            else:
                self.current_tiles = 3

    def render_surface(self):
        width = len(self.tiles[self.current_tiles])
        height = len(self.tiles[self.current_tiles][0])
        surface = pygame.Surface((width * TILESIZE, height * TILESIZE))
        for col in range(width):
            for row in range(height):
                if self.tiles[self.current_tiles][col][row]:
                    pygame.draw.rect(surface, get_block_color(self.color), (col * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE))

        return surface


class Tetromino_I(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_I)
        self.color = B_CYAN

    def rotate(self, playfield: list[list[int]], pos: tuple[int, int], counter_clockwise=False):
        pass


class Tetromino_O(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_O)
        self.color = B_YELLOW

    def rotate(self, playfield: list[list[int]], pos: tuple[int, int], counter_clockwise=False):
        pass


class Tetromino_T(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_T)


class Tetromino_S(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_S)


class Tetromino_Z(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_Z)


class Tetromino_J(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_J)


class Tetromino_L(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_L)
