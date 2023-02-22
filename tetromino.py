import pygame

TILESIZE = 32

B_EMPTY = 0
B_CYAN = 1  # I
B_YELLOW = 2  # O
B_PURPLE = 3  # T
B_GREEN = 4  # S
B_RED = 5  # Z
B_BLUE = 6  # J
B_ORANGE = 7  # L

B_IMG_CYAN = pygame.image.load("res/blocks/cyan.png")
B_IMG_YELLOW = pygame.image.load("res/blocks/yellow.png")
B_IMG_PURPLE = pygame.image.load("res/blocks/purple.png")
B_IMG_GREEN = pygame.image.load("res/blocks/green.png")
B_IMG_RED = pygame.image.load("res/blocks/red.png")
B_IMG_BLUE = pygame.image.load("res/blocks/blue.png")
B_IMG_ORANGE = pygame.image.load("res/blocks/orange.png")

B_IMG_GREY = pygame.image.load("res/blocks/grey.png")

# "rotated" -90
T_I = [
    [[False, False, False, False],
     [True, True, True, True],
     [False, False, False, False],
     [False, False, False, False]],

    [[False, False, True, False],
     [False, False, True, False],
     [False, False, True, False],
     [False, False, True, False]]
]
T_O = [
    [[True, True],
     [True, True]]
]
T_L = [
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
T_J = [
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
T_S = [
    [[True, True, False],
     [False, True, True],
     [False, False, False]],

    [[False, False, True],
     [False, True, True],
     [False, True, False]]
]
T_T = [
    [[False, True, False],
     [True, True, False],
     [False, True, False]],

    [[False, True, False],
     [True, True, True],
     [False, False, False]],

    [[False, True, False],
     [False, True, True],
     [False, True, False]],

    [[False, False, False],
     [True, True, True],
     [False, True, False]]
]
T_Z = [
    [[False, True, True],
     [True, True, False],
     [False, False, False]],

    [[False, True, False],
     [False, True, True],
     [False, False, True]]
]


def get_block_color(color_index):
    if color_index == B_CYAN:
        return B_IMG_CYAN
    if color_index == B_YELLOW:
        return B_IMG_YELLOW
    if color_index == B_RED:
        return B_IMG_RED
    if color_index == B_BLUE:
        return B_IMG_BLUE
    if color_index == B_GREEN:
        return B_IMG_GREEN
    if color_index == B_ORANGE:
        return B_IMG_ORANGE
    if color_index == B_PURPLE:
        return B_IMG_PURPLE

    return B_IMG_GREY


class TetrominoBase:

    def __init__(self, tiles: list[list[list[bool]]]):
        self.tiles = tiles
        self.current_tiles = 0
        self.color = -1

    def get_tiles(self):
        return self.tiles[self.current_tiles]

    def rotate(self, playfield: list[list[int]], current_pos: tuple[int, int], counter_clockwise=False):
        if counter_clockwise:
            i = 1
            while i < len(self.tiles):
                # print("i:", i, "len (modulo):", (len(self.tiles)), "result:", (self.current_tiles+i) % len(self.tiles))
                if self.can_rotate(playfield, current_pos, (self.current_tiles+i) % len(self.tiles)):
                    self.current_tiles = (self.current_tiles+i) % len(self.tiles)
                    break
                i += 1
        else:
            i = 1
            while i < len(self.tiles):
                # print("i:", i, "len (modulo):", (len(self.tiles)), "result:", (self.current_tiles - i) % len(self.tiles))
                if self.can_rotate(playfield, current_pos, (self.current_tiles - i) % len(self.tiles)):
                    self.current_tiles = (self.current_tiles - i) % len(self.tiles)
                    break
                i += 1

    def can_rotate(self, playfield: list[list[int]], current_pos: tuple[int, int], next_tiles_index: int):
        next_tiles = self.tiles[next_tiles_index]
        for col in range(len(next_tiles)):
            for row in range(len(next_tiles[0])):
                x = current_pos[0] + col
                y = current_pos[1] + row
                if next_tiles[col][row]:
                    # if OOB
                    if x < 0 or x >= len(playfield):
                        return False
                    # if block present
                    elif 0 <= x <= len(playfield)-1 and 0 <= y <= len(playfield[0])-1 and playfield[x][y] != B_EMPTY:
                        return False
        return True

    def can_move_left(self, playfield: list[list[int]], current_pos: tuple[int, int]):
        for col in range(len(self.get_tiles())):
            for row in range(len(self.get_tiles()[0])):
                x = current_pos[0] + col
                y = current_pos[1] + row
                if self.get_tiles()[col][row]:
                    # if OOB
                    if x == 0:
                        return False
                    # if block present
                    elif x > 0 and 0 <= y <= len(playfield[0])-1 and playfield[x-1][y] != B_EMPTY:
                        return False
        return True

    def can_move_right(self, playfield: list[list[int]], current_pos: tuple[int, int]):
        for col in range(len(self.get_tiles())):
            for row in range(len(self.get_tiles()[0])):
                x = current_pos[0] + col
                y = current_pos[1] + row
                if self.get_tiles()[col][row]:
                    # if OOB
                    if x == len(playfield)-1:
                        return False
                    # if block present
                    elif x <= len(playfield)-1 and 0 <= y <= len(playfield[0])-1 and playfield[x+1][y] != B_EMPTY:
                        return False
        return True

    def can_move_down(self, playfield: list[list[int]], current_pos: tuple[int, int]):
        for col in range(len(self.get_tiles())):
            for row in range(len(self.get_tiles()[0])):
                x = current_pos[0] + col
                y = current_pos[1] + row
                if self.get_tiles()[col][row]:
                    # if OOB
                    if y == len(playfield[0])-1:
                        return False
                    # if block present
                    if x <= len(playfield)-1 and y <= len(playfield[0])-1 and playfield[x][y+1] != B_EMPTY:
                        return False
        return True

    def render_surface(self):
        width = len(self.tiles[self.current_tiles])
        height = len(self.tiles[self.current_tiles][0])
        surface = pygame.Surface((width * TILESIZE, height * TILESIZE), pygame.SRCALPHA)
        for col in range(width):
            for row in range(height):
                if self.tiles[self.current_tiles][col][row]:
                    block_img = get_block_color(self.color)
                    block_img = pygame.transform.scale(block_img, (TILESIZE, TILESIZE))
                    surface.blit(block_img, (col * TILESIZE, row * TILESIZE))

        return surface


class Tetromino_I(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_I)
        self.color = B_CYAN


class Tetromino_O(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_O)
        self.color = B_YELLOW


class Tetromino_T(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_T)
        self.color = B_PURPLE


class Tetromino_S(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_S)
        self.color = B_GREEN


class Tetromino_Z(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_Z)
        self.color = B_RED


class Tetromino_J(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_J)
        self.color = B_BLUE


class Tetromino_L(TetrominoBase):

    def __init__(self):
        super().__init__(tiles=T_L)
        self.color = B_ORANGE
