import pygame
from pygame.font import Font

if not pygame.font.get_init():
    pygame.font.init()

DEFAULT_COLOR = (230, 230, 230)


def get_font(size):
    return Font("res/ARCADE_N.TTF", size)


def draw_text(text, x, y, surface: pygame.Surface, font: pygame.font.Font, color=DEFAULT_COLOR, shadow_color=DEFAULT_COLOR, shadow_offset=0):
    if shadow_offset > 0:
        surface.blit(font.render(text, True, shadow_color), (x, y+shadow_offset))
    surface.blit(font.render(text, True, color), (x, y))


def draw_text_individual(text, x, y, surface: pygame.Surface, font: pygame.font.Font, color=DEFAULT_COLOR, shadow_color=DEFAULT_COLOR, shadow_offset=0):
    i = 0
    while i < len(text):
        draw_text(text[i], x + (font.size("a")[0] * i), y, surface, font, color, shadow_color, shadow_offset)
        i += 1


def draw_aligned_text(text, center_x, y, surface: pygame.Surface, font: pygame.font.Font, color=DEFAULT_COLOR, shadow_color=DEFAULT_COLOR, shadow_offset=0):
    if shadow_offset > 0:
        shadow_text_surface = font.render(text, True, shadow_color)
        surface.blit(shadow_text_surface, (center_x - (shadow_text_surface.get_width() / 2), y+shadow_offset))
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (center_x - (text_surface.get_width() / 2), y))


def draw_centered_text(text, center_x, center_y, surface: pygame.Surface, font: pygame.font.Font, color=DEFAULT_COLOR, shadow_color=DEFAULT_COLOR, shadow_offset=0):
    if shadow_offset > 0:
        shadow_text_surface = font.render(text, True, shadow_color)
        surface.blit(shadow_text_surface, (center_x - (shadow_text_surface.get_width() / 2), center_y - (shadow_text_surface.get_height() / 2) + shadow_offset))
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (center_x - (text_surface.get_width() / 2), center_y - (text_surface.get_height() / 2)))


def draw_aligned_spaced_text(text, center_x, y, x_spacing, surface: pygame.Surface, font: pygame.font.Font, color=DEFAULT_COLOR, shadow_color=DEFAULT_COLOR, shadow_offset=0):
    width = font.size(text)[0] + (x_spacing*len(text))
    i = 0
    while i < len(text):
        draw_text(text[i], center_x-(width/2) + width/len(text)*i, y, surface, font, color, shadow_color, shadow_offset)
        i += 1
