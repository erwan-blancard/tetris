import pygame
import text
from button import ButtonSliderVertical


class ScrollingList:

    def __init__(self, x, y, width, height, color=(60, 60, 60)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_bar = ButtonSliderVertical(self.x + self.width - 4, self.y, self.height, 4)
        self.color = color

    def render(self, screen: pygame.Surface, itemlist: list, font: pygame.font.Font):
        screen.fill(self.color, (self.x, self.y, self.width, self.height))

        y_offset = font.size("a")[1]
        # create a Surface based of the length of the itemlist
        board = pygame.Surface((self.width - 8, y_offset * len(itemlist)))
        board.fill(self.color)
        for i in range(len(itemlist)):
            text.draw_text_individual(str(itemlist[i]), 2, y_offset * i, board, font)
        scroll_offset = 0
        if y_offset * len(itemlist) > self.height:
            scroll_offset = (board.get_height() - self.height) * self.scroll_bar.get_scroll_pos()
        screen.blit(board, (self.x, self.y), (0, scroll_offset, self.width, self.height))
        self.scroll_bar.render(screen)

    def mouse_input(self, event: pygame.event.Event):
        self.scroll_bar.mouse_input(event)
