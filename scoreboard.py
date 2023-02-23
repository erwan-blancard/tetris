import pygame
import game_state
import in_game
import text
from game_state import GameState
import score_utils
from button import ButtonLabel
from scrolling_list import ScrollingList
from playfield import ENDLESS, SURVIVAL, TIME_ATTACK


class ScoreBoardState(GameState):

    def __init__(self):
        super().__init__()
        window_bounds = pygame.display.get_window_size()
        self.scrolling_list = ScrollingList(32, window_bounds[1]/2, window_bounds[0]-64, window_bounds[1]/2-16, color=(50, 50, 50), alpha=120)
        self.list_gamemodes_score = [[], [], []]
        self.load_scores()

        self.gamemode_index = ENDLESS

        self.buttons = [
            ButtonLabel("Classique", self.scrolling_list.x, self.scrolling_list.y - 32, int(self.scrolling_list.width/3), 32, text.get_font(14), command=lambda: self.set_tab_endless()),
            ButtonLabel("Survie", self.scrolling_list.x + int(self.scrolling_list.width/3), self.scrolling_list.y - 32, int(self.scrolling_list.width/3), 32, text.get_font(14), command=lambda: self.set_tab_survivial()),
            ButtonLabel("Time Attack", self.scrolling_list.x + int((self.scrolling_list.width/3)*2), self.scrolling_list.y - 32, int(self.scrolling_list.width/3), 32, text.get_font(14), command=lambda: self.set_tab_time_attack())
        ]

    def load_scores(self):
        profiles = score_utils.get_profiles()
        endless_scores = []
        survival_scores = []
        time_attack_scores = []
        for profile_name in profiles:
            endless_scores.append([profile_name, score_utils.get_score(profile_name, ENDLESS)])
            survival_scores.append([profile_name, score_utils.get_score(profile_name, SURVIVAL)])
            time_attack_scores.append([profile_name, score_utils.get_score(profile_name, TIME_ATTACK)])

        def sorter(elem):
            return elem[1]

        endless_scores.sort(key=sorter, reverse=True)
        survival_scores.sort(key=sorter, reverse=True)
        time_attack_scores.sort(key=sorter, reverse=True)

        for i in range(len(endless_scores)):
            line = endless_scores[i][0]  # profile_name
            for j in range(18 - len(endless_scores[i][0])):
                line += " "
            score = endless_scores[i][1]
            if score < 0:
                score = "---"
            line += str(score)
            self.list_gamemodes_score[ENDLESS].append(line)
        for i in range(len(survival_scores)):
            line = survival_scores[i][0]        # profile_name
            for j in range(18 - len(survival_scores[i][0])):
                line += " "
            time = survival_scores[i][1]
            if time < 0:
                time = "---"
                line += str(time)
            else:
                line += in_game.format_time(time)
            self.list_gamemodes_score[SURVIVAL].append(line)
        for i in range(len(time_attack_scores)):
            line = time_attack_scores[i][0]        # profile_name
            for j in range(18 - len(time_attack_scores[i][0])):
                line += " "
            time = time_attack_scores[i][1]
            if time < 0:
                time = "---"
                line += str(time)
            else:
                line += in_game.format_time(time)
            self.list_gamemodes_score[TIME_ATTACK].append(line)

        # self.list_gamemodes_score = [endless_scores, survival_scores, time_attack_scores]

    def set_tab_endless(self):
        self.gamemode_index = ENDLESS
        self.scrolling_list.scroll_bar.set_scroll_pos(0)

    def set_tab_survivial(self):
        self.gamemode_index = SURVIVAL
        self.scrolling_list.scroll_bar.set_scroll_pos(0)

    def set_tab_time_attack(self):
        self.gamemode_index = TIME_ATTACK
        self.scrolling_list.scroll_bar.set_scroll_pos(0)

    def update(self):
        super().update()

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            surf = pygame.Surface((button.width, button.height), pygame.SRCALPHA)
            surf.set_alpha(self.scrolling_list.alpha)
            surf.fill((0, 0, 0))
            pygame.draw.line(surf, (255, 255, 255), (0, 0), (surf.get_width(), 0))
            pygame.draw.line(surf, (255, 255, 255), (0, button.height-1), (surf.get_width(), button.height-1))
            screen.blit(surf, (button.x, button.y))
        super().render(screen)

        text_first = "---"
        text_second = "---"
        text_third = "---"
        if len(self.list_gamemodes_score[self.gamemode_index]) > 0:
            text_first = self.list_gamemodes_score[self.gamemode_index][0]
        if len(self.list_gamemodes_score[self.gamemode_index]) > 1:
            text_second = self.list_gamemodes_score[self.gamemode_index][1]
        if len(self.list_gamemodes_score[self.gamemode_index]) > 2:
            text_third = self.list_gamemodes_score[self.gamemode_index][2]

        text.draw_text("1: " + text_first, 32, 164, screen, text.get_font(20), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=2)
        text.draw_text("2: " + text_second, 32+4, 164+32, screen, text.get_font(16), color=(216, 216, 216), shadow_color=(130, 130, 130), shadow_offset=2)
        text.draw_text("3: " + text_third, 32+6, 164+64, screen, text.get_font(14), color=(255, 130, 120), shadow_color=(193, 90, 54), shadow_offset=2)

        text.draw_centered_text("Tableau des scores", screen.get_width()/2, 64, screen, text.get_font(24), color=(255, 220, 30), shadow_color=(255, 140, 30), shadow_offset=3)
        self.scrolling_list.render(screen, self.list_gamemodes_score[self.gamemode_index], text.get_font(16), space_between_lines=16, x_offset=0)

    def input(self, event: pygame.event.Event):
        super().input(event)
        self.scrolling_list.mouse_input(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state.set_state(game_state.MENU)
