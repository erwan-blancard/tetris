import pygame
import score_utils
import text
import game_state
from game_state import ENDLESS, SURVIVAL, TIME_ATTACK
from button import ButtonLabel
from playfield import Playfield


def render_overlay(screen: pygame.Surface):
    rect_over = pygame.Surface((screen.get_width(), screen.get_height()))
    rect_over.set_alpha(150)
    rect_over.fill((40, 40, 40))
    screen.blit(rect_over, (0, 0))


class InGameState(game_state.GameState):

    def __init__(self, gamemode_type=ENDLESS):
        super().__init__()

        self.gamemode = gamemode_type

        self.paused = False

        self.playfield = Playfield(self.gamemode)

        window_bounds = pygame.display.get_window_size()
        self.buttons = [
            ButtonLabel("Continuer", window_bounds[0] / 2 - 109, window_bounds[1] / 2, 218, 24, font=text.get_font(24), command=lambda: self.close_pause_menu()),
            ButtonLabel("Recommencer", window_bounds[0] / 2 - 132, window_bounds[1] / 2 + 84, 264, 24, font=text.get_font(24), command=lambda: game_state.set_custom_ingame_state(self.playfield.gamemode)),
            ButtonLabel("Quitter", window_bounds[0] / 2 - 86, window_bounds[1] / 2 + 168, 172, 24, font=text.get_font(24), command=lambda: game_state.set_state(game_state.MENU))
        ]

        self.gameover_button = ButtonLabel("Recommencer", window_bounds[0] / 2 - 132, window_bounds[1] / 2 + 128, 264, 24, font=text.get_font(24), command=lambda: game_state.set_custom_ingame_state(self.playfield.gamemode))

    def update(self):
        super().update()
        if not self.paused:
            # update
            self.playfield.update()

    def render(self, screen: pygame.Surface):
        playfield_surface = self.playfield.render_surface()
        screen.blit(playfield_surface, (0, 0))

        if self.playfield.pending_tetromino is not None:
            pending_tetromino_surface = self.playfield.pending_tetromino.render_surface()
            screen.blit(pending_tetromino_surface, (playfield_surface.get_width() + 32, 48))

        if self.gamemode == ENDLESS:
            text.draw_text("Score: " + str(self.playfield.score), playfield_surface.get_width() + 32, 256, screen, text.get_font(16))
        elif self.gamemode == SURVIVAL or self.gamemode == TIME_ATTACK:
            text.draw_text("Chrono: " + str(self.playfield.timer), playfield_surface.get_width() + 32, 256, screen, text.get_font(10))

        if self.paused:
            render_overlay(screen)
            text.draw_centered_text("Pause", screen.get_width()/2, 92, screen, text.get_font(48))
            super().render(screen)

    def input(self, event: pygame.event.Event):
        if not self.paused:
            self.playfield.input(event)

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape":
                if self.paused:
                    self.paused = False
                else:
                    self.paused = True

        if self.paused:
            super().input(event)

    def close_pause_menu(self):
        self.paused = False
