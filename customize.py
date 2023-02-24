import game_state
from game_state import GameState, ENDLESS, SURVIVAL, TIME_ATTACK, MULTIPLAYER
from button import *
import text
import pygame


class CustomizeState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()

        self.gamemode_type = game_state.last_gamemode_type

        self.buttons = [
            ButtonLabel("Commencer", window_bounds[0]/2 - (284/2), window_bounds[1] - 72, 284, 32, text.get_font(32), command=lambda: self.set_ingame_state()),
            ButtonLabel("<", window_bounds[0] / 2 - 24 - 32 - 92-24, window_bounds[1] / 2 - 64, 32, 32, text.get_font(32), command=lambda: self.prev_gamemode()),
            ButtonLabel(">", window_bounds[0] / 2 + 24 + 92+24, window_bounds[1] / 2 - 64, 32, 32, text.get_font(32), command=lambda: self.next_gamemode())
        ]

        self.edit_P1_name = ButtonLabel("Modifier", 64, window_bounds[1] - 128, 132, 16, text.get_font(16), command=lambda: self.open_profile_shortcut())
        self.edit_P2_name = ButtonLabel("Modifier", window_bounds[0]-64-132, window_bounds[1] - 128, 132, 16, text.get_font(16), command=lambda: self.open_profile_shortcut(second_profile=True))

        self.show_profile_warning = False

        self.key_hints_solo = pygame.image.load("res/key_hints_solo.png")
        self.key_hints_solo = pygame.transform.scale(self.key_hints_solo, (self.key_hints_solo.get_width()*2, self.key_hints_solo.get_height()*2))

    def open_profile_shortcut(self, second_profile=False):
        game_state.last_gamemode_type = self.gamemode_type
        if second_profile:
            game_state.set_state(game_state.PROFILE_SHORTCUT_P2)
        else:
            game_state.set_state(game_state.PROFILE_SHORTCUT_P1)

    def next_gamemode(self):
        if self.gamemode_type < 3:
            self.gamemode_type += 1
        else:
            self.gamemode_type = 0

    def prev_gamemode(self):
        if self.gamemode_type > 0:
            self.gamemode_type -= 1
        else:
            self.gamemode_type = 3

    def set_ingame_state(self):
        if game_state.profile_name != game_state.second_profile_name:
            game_state.last_gamemode_type = self.gamemode_type
            game_state.set_custom_ingame_state(self.gamemode_type)

    def update(self):
        super().update()
        if game_state.profile_name == game_state.second_profile_name:
            self.show_profile_warning = True

    def render(self, screen: pygame.Surface):
        super().render(screen)
        if self.gamemode_type == MULTIPLAYER:
            self.edit_P1_name.render(screen)
            self.edit_P2_name.render(screen)
            text.draw_aligned_text(game_state.profile_name, 64+66, screen.get_height()-128-28, screen, text.get_font(20))
            text.draw_aligned_text(game_state.second_profile_name, screen.get_width() - 64 - 66, screen.get_height() - 128 - 28, screen, text.get_font(20))
            text.draw_aligned_text("VS", screen.get_width()/2, screen.get_height()-128-28, screen, text.get_font(40), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=5)
            if self.show_profile_warning:
                text.draw_aligned_text("Les noms de profil sont identiques !", screen.get_width() / 2, screen.get_height() - 128 - 64, screen, text.get_font(12), color=(255, 60, 60))
        else:
            screen.blit(self.key_hints_solo, (screen.get_width()/2-self.key_hints_solo.get_width()/2, screen.get_height()-128-72))
        text.draw_aligned_text("Modes de jeu", screen.get_width()/2, 24, screen, text.get_font(32), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=4)
        gamemode_text = str(self.gamemode_type)
        description = ["Description for gamemode " + str(self.gamemode_type)]
        if self.gamemode_type == ENDLESS:
            gamemode_text = "Classique"
            description = [
                "Le mode classique",
                "de Tetris !"]
        elif self.gamemode_type == SURVIVAL:
            gamemode_text = "Survie"
            description = ["Pas de score !",
                           "Seul le temps compte !"]
        elif self.gamemode_type == TIME_ATTACK:
            gamemode_text = "Time Attack"
            description = ["Effacez le plus",
                           "de lignes dans le",
                           "temps imparti !"]
        elif self.gamemode_type == MULTIPLAYER:
            gamemode_text = "1c1 Versus"
            description = ["Jouez avec un ami dans",
                           "ce mode 1c1 Versus !",
                           "Bloquez votre adversaire",
                           "en lui envoyant des blocs",
                           "en nettoyant vos lignes !"]
        text.draw_aligned_text(gamemode_text, screen.get_width() / 2, screen.get_height() / 2 - 64 + 4, screen, text.get_font(24))
        for i in range(len(description)):
            text.draw_aligned_text(description[i], screen.get_width() / 2, screen.get_height() / 2 + 32 + i*(28), screen, text.get_font(18))

    def input(self, event: pygame.event.Event):
        super().input(event)
        if self.gamemode_type == MULTIPLAYER:
            self.edit_P1_name.mouse_input(event)
            self.edit_P2_name.mouse_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state.set_state(game_state.MENU)
            elif event.key == pygame.K_RETURN:
                self.set_ingame_state()
            elif event.key == pygame.K_LEFT:
                self.prev_gamemode()
            elif event.key == pygame.K_RIGHT:
                self.next_gamemode()
