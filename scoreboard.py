import pygame
import game_state
import text
from game_state import GameState
import score_utils
from scrolling_list import ScrollingList


class ScoreBoardState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()
        self.scrolling_list = ScrollingList(32, 128, window_bounds[0]-64, window_bounds[1] - 128-16)
        self.score_list_formatted = []
        self.load_scores()

    def load_scores(self):
        profile_list = []
        profiles = score_utils.get_profiles()
        if profiles is not None:
            for profile_name in profiles:
                profile_list.append(profile_name)
        for profile in profile_list:
            score = score_utils.get_score(profile)
            string_formatted = profile
            for i in range(20 - len(profile)):
                string_formatted += " "
            string_formatted += str(score)
            self.score_list_formatted.append(string_formatted)

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        text.draw_centered_text("Tableau des scores", screen.get_width()/2, 64, screen, text.get_font(24), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=3)
        self.scrolling_list.render(screen, self.score_list_formatted, text.get_font(28))

    def input(self, event: pygame.event.Event):
        super().input(event)
        self.scrolling_list.mouse_input(event)
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "escape":
                game_state.set_state(game_state.MENU)
