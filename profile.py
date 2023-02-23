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
        self.next_state_id = game_state.MENU

    def validate_name(self):
        if len(self.profile_name_in) > 16:
            self.warning_text = "Le nom doit contenir au plus 16 characteres !"
        elif len(self.profile_name_in) >= 3:
            game_state.profile_name = self.profile_name_in
            score_utils.set_last_profile(game_state.profile_name)
            game_state.set_state(self.next_state_id)
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
            if event.key == pygame.K_ESCAPE:
                game_state.set_state(self.next_state_id)
            elif event.key == pygame.K_RETURN:
                self.validate_name()
            elif event.key == pygame.K_BACKSPACE:
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


class ProfileEditShortcutState(ProfileState):

    def __init__(self, second_profile=False):
        super().__init__()
        self.second_profile = second_profile
        self.next_state_id = game_state.CUSTOMIZE
        if self.second_profile:
            self.profile_name_in = game_state.second_profile_name

    def validate_name(self):
        if len(self.profile_name_in) > 16:
            self.warning_text = "Le nom doit contenir au plus 16 characteres !"
        elif len(self.profile_name_in) >= 3:
            if self.second_profile:
                game_state.second_profile_name = self.profile_name_in
                score_utils.set_last_second_profile(game_state.second_profile_name)
            else:
                game_state.profile_name = self.profile_name_in
                score_utils.set_last_profile(game_state.profile_name)
            game_state.set_state(self.next_state_id)
        else:
            self.warning_text = "Le nom doit contenir au moins 3 characteres !"

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            button.render(screen)
        text.draw_centered_text("Modifier le profil", screen.get_width() / 2, 64, screen, text.get_font(32), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=4)
        text.draw_centered_text(self.profile_name_in, screen.get_width() / 2, screen.get_height() / 2, screen, text.get_font(24))
        text.draw_centered_text(self.warning_text, screen.get_width() / 2, screen.get_height() / 2 + 72, screen, text.get_font(16), color=(255, 20, 20))
