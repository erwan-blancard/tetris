import pygame

import score_utils
import text
import game_state
from button import ButtonLabel


class ProfileState(game_state.GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()
        self.buttons = [
            ButtonLabel("Valider le nom", window_bounds[0] / 2 - 170, window_bounds[1] / 2 + 128, 340, 32, font=text.get_font(24), command=lambda: self.validate_name())
        ]
        self.profile_name_in = game_state.profile_name
        self.warning_text = ""

    def validate_name(self):
        if len(self.profile_name_in) > 16:
            self.warning_text = "Le nom doit contenir au plus 16 characteres !"
        elif len(self.profile_name_in) >= 3:
            game_state.profile_name = self.profile_name_in
            score_utils.set_last_profile(game_state.profile_name)
            game_state.set_state(game_state.MENU)
        else:
            self.warning_text = "Le nom doit contenir au moins 3 characteres !"

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_centered_text("Profil", screen.get_width() / 2, 64, screen, text.get_font(48), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=6)
        text.draw_centered_text(self.profile_name_in, screen.get_width() / 2, screen.get_height() / 2, screen, text.get_font(24))
        text.draw_centered_text(self.warning_text, screen.get_width() / 2, screen.get_height() / 2 + 72, screen, text.get_font(16), color=(255, 20, 20))

    def input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            key_input = pygame.key.name(event.key)
            if key_input == "escape":
                game_state.set_state(game_state.MENU)
            elif key_input == "return":
                self.validate_name()
            elif key_input == "backspace":
                self.profile_name_in = self.profile_name_in[:-1]
            else:
                if not len(self.profile_name_in) >= 16:
                    if key_input in "abcdefghijklmnopqrstuvwxyz":
                        self.profile_name_in += key_input
                    elif key_input == "space":
                        self.profile_name_in += " "
                    elif key_input in ["[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]:
                        self.profile_name_in += key_input[1:2]
        super().input(event)
