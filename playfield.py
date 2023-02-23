import time

import tetromino
from tetromino import *
from game_state import ENDLESS, SURVIVAL, TIME_ATTACK, MULTIPLAYER
import text
import pygame
import random

WIDTH = 10
HEIGHT = 20

CONTROL_METHOD_SOLO = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_q, pygame.K_d]
CONTROL_METHOD_1 = [pygame.K_q, pygame.K_d, pygame.K_s, pygame.K_r, pygame.K_t]
CONTROL_METHOD_2 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_1, pygame.K_2]
LEFT = 0
RIGHT = 1
DOWN = 2
ROT_LEFT = 3
ROT_RIGHT = 4


class Playfield:

    def __init__(self, gamemode=ENDLESS, alternative_control_method=False):
        # Time Before Update
        self.TBU = 0.4      # 0.5
        self.last_update: float = 0
        self.tilesize = TILESIZE

        self.gamemode = gamemode

        self.control_keys = CONTROL_METHOD_SOLO
        if self.gamemode == MULTIPLAYER:
            self.tilesize = 20
            self.pending_badlines = 0
            if alternative_control_method:
                self.control_keys = CONTROL_METHOD_2
            else:
                self.control_keys = CONTROL_METHOD_1

        if self.gamemode == SURVIVAL:
            self.begining_timer = time.time()
            self.timer = 0.0
        elif self.gamemode == TIME_ATTACK:
            self.begining_timer = time.time()
            self.total_time = 60.0*4
            self.timer = self.total_time
            self.lines_cleared = 0

        self.rotate = 0

        self.blocks: list[list[int]] = []
        for col in range(WIDTH):
            self.blocks.append([])
            for row in range(HEIGHT):
                self.blocks[col].append(0)

        self.score = 0
        self.turns = 0
        self.stop = False

        self.current_tetromino: TetrominoBase = None
        self.current_tetromino_pos: tuple[int, int] = (0, 0)
        self.pending_tetromino: TetrominoBase = None

        self.init_playfield()

    def init_playfield(self):
        self.current_tetromino = new_tetromino(self.tilesize)
        self.current_tetromino_pos = (4, -1)
        self.pending_tetromino = new_tetromino(self.tilesize)

    def update(self):
        if not self.stop and (self.gamemode == TIME_ATTACK or self.gamemode == SURVIVAL):
            self.update_timer()
            # if time limit is reached in TIME ATTACK
            if self.gamemode == TIME_ATTACK and self.timer <= 0:
                self.stop = True
                self.timer = 0
        if not self.stop and time.time() > self.last_update + self.TBU:
            self.last_update = time.time()
            # update tetromino
            if self.current_tetromino.can_move_down(self.blocks, self.current_tetromino_pos):
                self.current_tetromino_pos = (self.current_tetromino_pos[0], self.current_tetromino_pos[1]+1)
            else:
                self.print_tetromino_on_board()
                self.update_lines()
                self.spawn_next_tetrominos()
                self.turns += 1
                self.update_TBU()

    def render_surface(self):
        surface = pygame.Surface((WIDTH*self.tilesize, HEIGHT*self.tilesize), pygame.SRCALPHA)
        rect_over = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        rect_over.set_alpha(150)
        rect_over.fill((30, 30, 30))
        surface.blit(rect_over, (0, 0))
        for col in range(WIDTH):
            for row in range(HEIGHT):
                pygame.draw.rect(surface, (60, 60, 60), (col*self.tilesize, row*self.tilesize, self.tilesize, self.tilesize), width=1)
                if self.blocks[col][row] != 0:
                    block_img = self.get_block_color(col, row)
                    block_img = pygame.transform.scale(block_img, (self.tilesize, self.tilesize))
                    surface.blit(block_img, (col*self.tilesize, row*self.tilesize))

        if self.current_tetromino is not None:
            tetromino_surface = self.current_tetromino.render_surface()
            surface.blit(tetromino_surface, (self.current_tetromino_pos[0]*self.tilesize, self.current_tetromino_pos[1]*self.tilesize))

        return surface

    def input(self, event: pygame.event):
        if not self.stop and event.type == pygame.KEYDOWN:
            if event.key == self.control_keys[ROT_LEFT]:
                if self.current_tetromino is not None:
                    self.current_tetromino.rotate(self.blocks, self.current_tetromino_pos, counter_clockwise=True)
            elif event.key == self.control_keys[ROT_RIGHT]:
                if self.current_tetromino is not None:
                    self.current_tetromino.rotate(self.blocks, self.current_tetromino_pos)
            elif event.key == self.control_keys[LEFT]:
                self.move_tetromino()
            elif event.key == self.control_keys[RIGHT]:
                self.move_tetromino(right=True)
            elif event.key == self.control_keys[DOWN]:
                self.fast_fall_tetromino()

    def add_points_by_combo(self, num_rows: int):
        if self.gamemode == TIME_ATTACK:
            self.lines_cleared += num_rows
        elif self.gamemode == ENDLESS:
            self.score += (num_rows+(num_rows//4))*100

    def get_block_color(self, col, row):
        color_index = self.blocks[col][row]
        return tetromino.get_block_color(color_index)
