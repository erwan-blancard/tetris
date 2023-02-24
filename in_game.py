import pygame
import score_utils
import text
import game_state
from game_state import ENDLESS, SURVIVAL, TIME_ATTACK, MULTIPLAYER
from button import ButtonLabel
from playfield import Playfield


def render_overlay(screen: pygame.Surface):
    rect_over = pygame.Surface((screen.get_width(), screen.get_height()))
    rect_over.set_alpha(150)
    rect_over.fill((40, 40, 40))
    screen.blit(rect_over, (0, 0))


def format_time(time: float):
    minutes = str(int(time // 60))
    seconds = str(round(int(time) % 60, 0))
    if len(minutes) < 2:
        minutes = "0" + minutes
    if len(seconds) < 2:
        seconds = "0" + seconds

    return minutes + ":" + seconds


class InGameState(game_state.GameState):

    def __init__(self, gamemode_type=ENDLESS):
        super().__init__()

        self.gamemode = gamemode_type

        self.paused = False

        self.playfield = Playfield(self.gamemode)

        if self.gamemode == MULTIPLAYER:
            self.second_playfield = Playfield(self.gamemode, alternative_control_method=True)
            self.playfield_last_turn = 0
            self.second_playfield_last_turn = 0

        window_bounds = pygame.display.get_window_size()
        self.buttons = [
            ButtonLabel("Continuer", window_bounds[0] / 2 - 109, window_bounds[1] / 2, 218, 24, font=text.get_font(24), command=lambda: self.close_pause_menu()),
            ButtonLabel("Recommencer", window_bounds[0] / 2 - 132, window_bounds[1] / 2 + 84, 264, 24, font=text.get_font(24), command=lambda: game_state.set_custom_ingame_state(self.playfield.gamemode)),
            ButtonLabel("Quitter", window_bounds[0] / 2 - 86, window_bounds[1] / 2 + 168, 172, 24, font=text.get_font(24), command=lambda: game_state.set_state(game_state.MENU))
        ]

        self.add_score_check = False
        self.retry_button = ButtonLabel("Recommencer", window_bounds[0] / 2 - 132, window_bounds[1] / 2 + 128, 264, 24, font=text.get_font(24), command=lambda: game_state.set_custom_ingame_state(self.playfield.gamemode))
        self.quit_button = ButtonLabel("Quitter", window_bounds[0] / 2 - 86, window_bounds[1] / 2 + 232, 172, 24, font=text.get_font(24), command=lambda: game_state.set_state(game_state.MENU))

    def update(self):
        super().update()
        if not self.paused:
            # update
            if not self.is_game_over():
                self.playfield.update()
                if self.gamemode == MULTIPLAYER:
                    self.second_playfield.update()
                    # check badlines
                    if self.playfield.turns > self.playfield_last_turn:
                        self.second_playfield.pending_badlines += self.playfield.next_opponent_badlines
                        self.playfield.next_opponent_badlines = 0
                    if self.second_playfield.turns > self.second_playfield_last_turn:
                        self.playfield.pending_badlines += self.second_playfield.next_opponent_badlines
                        self.second_playfield.next_opponent_badlines = 0
            else:
                if not self.add_score_check:
                    if self.gamemode == ENDLESS:
                        if score_utils.get_score(game_state.profile_name, self.gamemode) < self.playfield.score:
                            score_utils.add_score(game_state.profile_name, self.gamemode, self.playfield.score)
                    elif self.gamemode == SURVIVAL:
                        if score_utils.get_score(game_state.profile_name, self.gamemode) < self.playfield.timer:
                            score_utils.add_score(game_state.profile_name, self.gamemode, self.playfield.timer)
                    elif self.gamemode == TIME_ATTACK:
                        if score_utils.get_score(game_state.profile_name, self.gamemode) < self.playfield.lines_cleared:
                            score_utils.add_score(game_state.profile_name, self.gamemode, self.playfield.lines_cleared)
                    self.add_score_check = True

    def render(self, screen: pygame.Surface):
        playfield_surface = self.playfield.render_surface()
        second_playfield_surface = None
        if self.gamemode == MULTIPLAYER:
            second_playfield_surface = self.second_playfield.render_surface()
        if self.gamemode == ENDLESS or self.gamemode == SURVIVAL or self.gamemode == TIME_ATTACK:
            screen.blit(playfield_surface, (screen.get_width() - playfield_surface.get_width() - 83, 70))
        if self.gamemode == MULTIPLAYER:
            screen.blit(playfield_surface, (50, 200))
            screen.blit(second_playfield_surface, (screen.get_width() - second_playfield_surface.get_width() - 50, 200))

        if self.gamemode == ENDLESS or self.gamemode == SURVIVAL or self.gamemode == TIME_ATTACK:
            if self.playfield.pending_tetromino is not None:
                pending_tetromino_surface = self.playfield.pending_tetromino.render_surface()
                screen.blit(pending_tetromino_surface, (50, 150))

        if self.gamemode == MULTIPLAYER:
            text.draw_aligned_text(game_state.profile_name, 50+playfield_surface.get_width()/2, 20, screen, text.get_font(16))
            text.draw_aligned_text(game_state.second_profile_name, screen.get_width() - second_playfield_surface.get_width()/2 - 50, 20, screen, text.get_font(16))
            if self.playfield.pending_tetromino is not None:
                pending_tetromino_surface = self.playfield.pending_tetromino.render_surface()
                screen.blit(pending_tetromino_surface, (130, 80))
            if self.second_playfield.pending_tetromino is not None:
                pending_tetromino_surface = self.second_playfield.pending_tetromino.render_surface()
                screen.blit(pending_tetromino_surface, (408, 80))

        if self.gamemode == ENDLESS:
            text.draw_aligned_text("Score: " + str(self.playfield.score), screen.get_width() - playfield_surface.get_width()/2 - 83, 43, screen, text.get_font(16))
        elif self.gamemode == SURVIVAL:
            text.draw_aligned_text("Chrono: " + format_time(self.playfield.timer), screen.get_width() - playfield_surface.get_width()/2 - 83, 43, screen, text.get_font(16))
        elif self.gamemode == TIME_ATTACK:
            text.draw_aligned_text("Lignes: " + str(self.playfield.lines_cleared), screen.get_width() - playfield_surface.get_width()/2 - 83, 43-24, screen, text.get_font(10))
            text.draw_aligned_text("Chrono: " + format_time(self.playfield.timer), screen.get_width() - playfield_surface.get_width()/2 - 83, 43, screen, text.get_font(10))

        if self.is_game_over():
            render_overlay(screen)
            text.draw_centered_text("Game Over!", screen.get_width() / 2, 128, screen, text.get_font(48), color=(0, 190, 255), shadow_color=(0, 100, 255), shadow_offset=6)
            self.retry_button.render(screen)
            self.quit_button.render(screen)
            if self.gamemode == ENDLESS:
                text.draw_centered_text("Score: " + str(self.playfield.score), screen.get_width() / 2, screen.get_height() / 2 - 64, screen, text.get_font(32), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=4)
            elif self.gamemode == SURVIVAL:
                text.draw_centered_text("Temps: " + format_time(self.playfield.timer), screen.get_width() / 2, screen.get_height() / 2 - 64, screen, text.get_font(32), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=4)
            elif self.gamemode == TIME_ATTACK:
                text.draw_centered_text("Lignes: " + str(self.playfield.lines_cleared), screen.get_width() / 2, screen.get_height() / 2 - 64, screen, text.get_font(32), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=4)
            elif self.gamemode == MULTIPLAYER:
                player_name = "missingno"
                if self.playfield.stop:
                    player_name = game_state.second_profile_name
                elif self.second_playfield.stop:
                    player_name = game_state.profile_name
                text.draw_centered_text("Victoire de", screen.get_width() / 2, screen.get_height() / 2 - 64, screen, text.get_font(24), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=3)
                text.draw_centered_text(player_name + " !", screen.get_width() / 2, screen.get_height() / 2 - 24, screen, text.get_font(24), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=3)

        if self.paused:
            render_overlay(screen)
            text.draw_centered_text("Pause", screen.get_width()/2, 92, screen, text.get_font(48))
            super().render(screen)

    def input(self, event: pygame.event.Event):
        if not self.paused:
            if not self.is_game_over():
                self.playfield.input(event)
                if self.gamemode == MULTIPLAYER:
                    self.second_playfield.input(event)

        if not self.is_game_over():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
        else:
            self.retry_button.mouse_input(event)
            self.quit_button.mouse_input(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state.set_custom_ingame_state(self.playfield.gamemode)
                elif event.key == pygame.K_ESCAPE:
                    game_state.set_state(game_state.MENU)

        if self.paused:
            super().input(event)

    def is_game_over(self):
        if self.gamemode == ENDLESS or self.gamemode == TIME_ATTACK or self.gamemode == SURVIVAL:
            return self.playfield.stop
        elif self.gamemode == MULTIPLAYER:
            return (self.playfield.stop or self.second_playfield.stop)
        return False

    def close_pause_menu(self):
        self.paused = False
