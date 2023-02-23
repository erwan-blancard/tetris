import pygame
import text
from button import ButtonSliderVertical


class ScrollingList:

    def __init__(self, x, y, width, height, color=(60, 60, 60), alpha=255):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_bar = ButtonSliderVertical(self.x + self.width - 4, self.y, self.height, 4)
        self.color = color
        self.alpha = alpha

    def render(self, screen: pygame.Surface, itemlist: list, font: pygame.font.Font, space_between_lines=0, x_offset=0):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surf.set_alpha(self.alpha)
        surf.fill(self.color)
        screen.blit(surf, (self.x, self.y))

        y_offset = font.size("a")[1]+space_between_lines
        # create a Surface based of the length of the itemlist
        board = pygame.Surface((self.width - 8 - x_offset, y_offset * len(itemlist)), pygame.SRCALPHA)
        for i in range(len(itemlist)):
            text.draw_text_individual(str(itemlist[i]), 2, y_offset * i, board, font)
        scroll_offset = 0
        if y_offset * len(itemlist) > self.height:
            scroll_offset = (board.get_height() - self.height) * self.scroll_bar.get_scroll_pos()
        screen.blit(board, (self.x + x_offset, self.y), (0, scroll_offset, self.width, self.height))
        self.scroll_bar.render(screen)

    def mouse_input(self, event: pygame.event.Event):
        self.scroll_bar.mouse_input(event)
