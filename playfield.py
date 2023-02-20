import time

import pygame


TILESIZE = 16
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

        self.score = 0

    def update(self, key_input: str):
        if time.time() > self.last_update + self.TBU:
            self.last_update = time.time()
            # update

    def render(self, screen: pygame.Surface):
        pass

    def add_points_by_combo(self, num_rows: int):
        self.score += (num_rows+(num_rows//4))*100
