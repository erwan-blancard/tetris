import time
from tetromino import *
import text
import pygame
import random

TILESIZE = 24
WIDTH = 10
HEIGHT = 40     # 20 visibles


class Playfield:

    def __init__(self):
        # Time Before Update
        self.TBU = 0.5
        self.last_update: float = 0

        self.blocks: list[list[int]] = []
        for col in range(WIDTH):
            self.blocks.append([])
            for row in range(HEIGHT):
                self.blocks[col].append(0)
                # self.blocks[col].append(random.randint(0, 7))

        self.score = 0

        self.current_tetromino: TetrominoBase = None
        self.current_tetromino_pos: tuple[int, int] = (4, 22)
        self.pending_tetromino: TetrominoBase = None

    def update(self):
        if time.time() > self.last_update + self.TBU:
            self.last_update = time.time()
            # update

    def render_surface(self):
        surface = pygame.Surface((WIDTH*TILESIZE, 20*TILESIZE))
        for col in range(WIDTH):
            for row in range(20):
                pygame.draw.rect(surface, self.get_block_color(col, row), (col*TILESIZE, (20-row)*TILESIZE, TILESIZE, TILESIZE))
                text.draw_text(str(col) + ";" + str(row), col*TILESIZE, (20-row)*TILESIZE, surface, text.get_font(8), (255, 255, 255))

        return surface

    def input(self, event: pygame.event):
        pass

    def add_points_by_combo(self, num_rows: int):
        self.score += (num_rows+(num_rows//4))*100

    def get_block_color(self, col, row):
        color_index = self.blocks[col][row]
        if color_index == B_EMPTY:
            return 0, 0, 0
        elif color_index == B_CYAN:
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
