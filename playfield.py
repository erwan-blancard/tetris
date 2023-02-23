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

    def spawn_next_tetrominos(self):
        self.current_tetromino = self.pending_tetromino
        self.current_tetromino_pos = (4, -1)

        offset = 0
        while offset < 3:
            if not self.current_tetromino.can_rotate(self.blocks, (4, -1 - offset), self.current_tetromino.current_tiles):
                offset += 1
            else:
                break
        self.current_tetromino_pos = (4, -1 - offset)

        self.pending_tetromino = new_tetromino(self.tilesize)

    def move_tetromino(self, right=False):
        if self.current_tetromino is not None:
            if right:
                if self.current_tetromino.can_move_right(self.blocks, self.current_tetromino_pos):
                    self.current_tetromino_pos = (self.current_tetromino_pos[0] + 1, self.current_tetromino_pos[1])
            elif self.current_tetromino.can_move_left(self.blocks, self.current_tetromino_pos):
                self.current_tetromino_pos = (self.current_tetromino_pos[0] - 1, self.current_tetromino_pos[1])

    def print_tetromino_on_board(self):
        one_printed = False
        for col in range(len(self.current_tetromino.get_tiles())):
            for row in range(len(self.current_tetromino.get_tiles()[0])):
                if self.current_tetromino.get_tiles()[col][row]:
                    x = self.current_tetromino_pos[0] + col
                    y = self.current_tetromino_pos[1] + row
                    if 0 <= x < len(self.blocks) and 0 <= y < len(self.blocks[0]):
                        self.blocks[x][y] = self.current_tetromino.color
                        one_printed = True
        # stops the game (game over) if no blocks of the tetromino can be printed on the block list
        if not one_printed:
            self.stop = True

    def update_TBU(self):
        if self.turns < 70*3:
            self.TBU = 0.5 - (self.turns // 70)*0.1
        else:
            self.TBU = 0.08

    def update_timer(self):
        if self.gamemode == SURVIVAL:
            self.timer = time.time() - self.begining_timer
        elif self.gamemode == TIME_ATTACK:
            self.timer = self.total_time - (time.time() - self.begining_timer)

    def fast_fall_tetromino(self):
        if self.current_tetromino is not None:
            for i in range(len(self.blocks[0])):
                if not self.current_tetromino.can_move_down(self.blocks, (self.current_tetromino_pos[0], self.current_tetromino_pos[1]+i)):
                    self.current_tetromino_pos = (self.current_tetromino_pos[0], self.current_tetromino_pos[1]+i)
                    self.last_update = 0
                    break

    def update_lines(self):
        list_rows_filled = []
        for row in range(len(self.blocks[0])):
            row_filled = True
            for col in range(len(self.blocks)):
                if self.blocks[col][row] == 0:
                    row_filled = False
                    break
            if row_filled:
                list_rows_filled.append(row)
        if len(list_rows_filled) > 0:
            self.clear_lines(list_rows_filled)
            self.add_points_by_combo(len(list_rows_filled))

    def clear_lines(self, rows_filled: list[int]):
        new_blocks: list[list[int]] = []
        rows_chained = 0
        for col in range(len(self.blocks)):
            new_blocks.append([])
            for row in range(len(self.blocks[0])):
                new_blocks[col].append(0)

        for row in range(len(self.blocks[0])):
            if (len(self.blocks[0])-row-1) in rows_filled:
                rows_chained += 1
            else:
                for col in range(len(self.blocks)):
                    new_blocks[col][(len(self.blocks[0])-row-1)+rows_chained] = self.blocks[col][(len(self.blocks[0])-row-1)]

        self.blocks = new_blocks
