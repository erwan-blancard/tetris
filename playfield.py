import time

import tetromino
from tetromino import *
import text
import pygame
import random

WIDTH = 10
HEIGHT = 20


def new_tetromino():
    new_t = Tetromino_O()
    return new_t


class Playfield:

    def __init__(self):
        # Time Before Update
        self.TBU = 0.5
        self.last_update: float = 0

        self.rotate = 0

        self.blocks: list[list[int]] = []
        for col in range(WIDTH):
            self.blocks.append([])
            for row in range(HEIGHT):
                self.blocks[col].append(0)
                # self.blocks[col].append(random.randint(0, 7))

        self.score = 0

        self.current_tetromino: TetrominoBase = None
        self.current_tetromino_pos: tuple[int, int] = (0, 0)
        self.pending_tetromino: TetrominoBase = None

        self.init_playfield()

    def init_playfield(self):
        self.current_tetromino = new_tetromino()
        self.current_tetromino_pos = (4, 0)
        self.pending_tetromino = new_tetromino()

    def update(self):
        if time.time() > self.last_update + self.TBU:
            self.last_update = time.time()
            # update

    def render_surface(self):
        surface = pygame.Surface((WIDTH*TILESIZE, 20*TILESIZE))
        surface.fill((0, 0, 0))
        for col in range(WIDTH):
            for row in range(HEIGHT):
                pygame.draw.rect(surface, self.get_block_color(col, row), (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                pygame.draw.rect(surface, (255, 255, 255), (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE), width=1)
                text.draw_text(str(col) + ";" + str(row), col*TILESIZE, row*TILESIZE, surface, text.get_font(8), (255, 255, 255))

        if self.current_tetromino is not None:
            tetromino_surface = self.current_tetromino.render_surface()
            surface.blit(tetromino_surface, (self.current_tetromino_pos[0]*TILESIZE, self.current_tetromino_pos[1]*TILESIZE))

        return surface

    def input(self, event: pygame.event):
        pass

    def add_points_by_combo(self, num_rows: int):
        self.score += (num_rows+(num_rows//4))*100

    def get_block_color(self, col, row):
        color_index = self.blocks[col][row]
        return tetromino.get_block_color(color_index)
