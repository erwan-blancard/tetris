import math
import time

import pygame
import game_state
import text
from game_state import GameState
from button import ButtonLabel, ButtonIcon


class MenuState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()
        self.buttons += [
            ButtonLabel("Jouer", window_bounds[0] / 2 - 60, window_bounds[1] / 2 + 60, 120, 32, font=text.get_font(24), command=lambda: game_state.set_state(game_state.CUSTOMIZE)),
            ButtonLabel("Scoreboard", window_bounds[0]/2 - 120, window_bounds[1] / 2 + 148, 240, 32, font=text.get_font(24), command=lambda: game_state.set_state(game_state.SCOREBOARD)),
            ButtonLabel("Profil", window_bounds[0]/2 - 74, window_bounds[1] / 2 + 148 + 88, 148, 32, font=text.get_font(24), command=lambda: game_state.set_state(game_state.PROFILE))
        ]
        self.titlelogo = pygame.image.load("res/logo.png")
        self.titlelogo = pygame.transform.scale(self.titlelogo, (136*3, 40*3))

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.blit(self.titlelogo, (screen.get_width()/2 - self.titlelogo.get_width()/2, 72))
        text.draw_text(game_state.profile_name, 8, screen.get_height() - 24, screen, text.get_font(16))

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "return":
                game_state.set_state(game_state.CUSTOMIZE)
