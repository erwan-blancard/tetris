from tetromino import *
import pygame
import random


class AnimatedBackground:

    def __init__(self):
        self.tetromino_list: list[TetrominoBase] = []
        self.tetromino_attributes_list: list[list[float]] = []     # x, y, speed
        for i in range(9):
            self.add_tetromino(randomize_height=True)

    def update(self):
        tetrominos_to_remove = []
        for i in range(len(self.tetromino_attributes_list)):
            if self.tetromino_attributes_list[i][1] >= pygame.display.get_window_size()[1]:
                tetrominos_to_remove.append(i)
            else:
                self.tetromino_attributes_list[i][1] += self.tetromino_attributes_list[i][2]
        tetrominos_to_remove.sort(reverse=True)
        for i in tetrominos_to_remove:
            self.tetromino_list.pop(i)
            self.tetromino_attributes_list.pop(i)
        for i in range(len(tetrominos_to_remove)):
            self.add_tetromino()

    def render(self, screen: pygame.Surface):
        surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        surface.set_alpha(60)
        for i in range(len(self.tetromino_list)):
            surface.blit(self.tetromino_list[i].render_surface(), (int(self.tetromino_attributes_list[i][0]), int(self.tetromino_attributes_list[i][1])))
        screen.blit(surface, (0, 0))

    def add_tetromino(self, randomize_height=False):
        self.tetromino_list.insert(0, new_tetromino(random.randint(2, 8)*4, randomize_orientation=True))
        y = 0
        offset = self.tetromino_list[0].render_surface().get_height()
        if randomize_height:
            y = random.randint(0, pygame.display.get_window_size()[1]-offset)
        self.tetromino_attributes_list.insert(0, [random.randint(0, (pygame.display.get_window_size()[0]-offset)), -offset+y, random.random()+0.1])
