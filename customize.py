import os

import game_state
from game_state import GameState, ENDLESS, SURVIVAL, TIME_ATTACK
from button import *
import text
import pygame


class CustomizeState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()

        self.gamemode_type = ENDLESS

        self.buttons = [
            ButtonLabel("Commencer", window_bounds[0]/2 - (284/2), window_bounds[1] - 72, 284, 32, text.get_font(32), command=lambda: game_state.set_custom_ingame_state(self.gamemode_type)),
            ButtonLabel("<", window_bounds[0] / 2 - 24 - 32 - 92-24, window_bounds[1] / 2 - 64, 32, 32, text.get_font(32), command=lambda: self.prev_gamemode()),
            ButtonLabel(">", window_bounds[0] / 2 + 24 + 92+24, window_bounds[1] / 2 - 64, 32, 32, text.get_font(32), command=lambda: self.next_gamemode())
        ]

    def next_gamemode(self):
        if self.gamemode_type < 2:
            self.gamemode_type += 1
        else:
            self.gamemode_type = 0

    def prev_gamemode(self):
        if self.gamemode_type > 0:
            self.gamemode_type -= 1
        else:
            self.gamemode_type = 2

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_aligned_text("Modes de jeu", screen.get_width()/2, 24, screen, text.get_font(32), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=4)
        gamemode_text = str(self.gamemode_type)
        description = ["Description for gamemode " + str(self.gamemode_type)]
        if self.gamemode_type == 0:
            gamemode_text = "Classique"
            description = ["Le mode classique", "de Tetris !"]
        elif self.gamemode_type == 1:
            gamemode_text = "Survie"
            description = ["Essayez de survivre", "le plus longtemps possible !"]
        elif self.gamemode_type == 2:
            gamemode_text = "Time Attack"
            description = ["Effacez le plus", "de lignes dans le", "temps imparti !"]
        text.draw_aligned_text(gamemode_text, screen.get_width() / 2, screen.get_height() / 2 - 64 + 4, screen, text.get_font(24))
        for i in range(len(description)):
            text.draw_aligned_text(description[i], screen.get_width() / 2, screen.get_height() / 2 + 32 + i*(28), screen, text.get_font(18))

    def input(self, event: pygame.event.Event):
        super().input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state.set_state(game_state.MENU)
            elif event.key == pygame.K_RETURN:
                game_state.set_custom_ingame_state(self.gamemode_type)
            elif event.key == pygame.K_LEFT:
                self.prev_gamemode()
            elif event.key == pygame.K_RIGHT:
                self.next_gamemode()
