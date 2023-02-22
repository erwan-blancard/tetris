import os

import game_state
from game_state import GameState
from button import *
import text
import pygame


class CustomizeState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()

        self.buttons = [
            ButtonLabel("Commencer", window_bounds[0]/2 - (284/2), window_bounds[1] - 72, 284, 32, text.get_font(32), command=lambda: game_state.set_state(game_state.INGAME))
        ]

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_aligned_text("Modes de jeu", screen.get_width()/2, 24, screen, text.get_font(32), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=4)

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape":
                game_state.set_state(game_state.MENU)
            elif pygame.key.name(event.key) == "return":
                game_state.set_state(game_state.INGAME)
