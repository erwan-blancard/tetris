import pygame
import text


class BaseButton:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mouse_inside = False
        self.mouse_clicked = False

    def render(self, screen: pygame.Surface):
        # pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), width=1)
        pass

    def mouse_input(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if (self.x <= mouse_pos[0] <= self.x + self.width) and (self.y <= mouse_pos[1] <= self.y + self.height):
            self.mouse_inside = True
        else:
            self.mouse_inside = False

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            self.mouse_clicked = True
        else:
            self.mouse_clicked = False

    def execute(self):
        pass


class ButtonLabel(BaseButton):

    def __init__(self, label, x, y, width, height, font: pygame.font.Font = None, command=None):
        super().__init__(x, y, width, height)
        self.label = label
        if font is not None:
            self.font = font
        else:
            self.font = pygame.font.Font(None, height)
        self.command = command

    def render(self, screen: pygame.Surface):
        text.draw_centered_text(self.label, self.x+(self.width/2), self.y+(self.height/2), screen, self.font)
        super().render(screen)

    def mouse_input(self, event: pygame.event.Event):
        super().mouse_input(event)
        if self.mouse_inside and self.mouse_clicked:
            self.execute()

    def execute(self):
        if self.command is not None:
            self.command()


class ButtonIcon(BaseButton):

    def __init__(self, x, y, size, icon, command=None):
        super().__init__(x, y, size, size)
        self.command = command
        icon = pygame.transform.scale(icon, (self.width, self.height))
        self.icon = icon

    def render(self, screen):
        screen.blit(self.icon, (self.x, self.y))
        super().render(screen)

    def mouse_input(self, event: pygame.event.Event):
        super().mouse_input(event)
        if self.mouse_inside and self.mouse_clicked:
            self.execute()

    def execute(self):
        if self.command is not None:
            self.command()


class TrueFalseButton(BaseButton):

    def __init__(self, x, y, size, false_icon: pygame.Surface, true_icon: pygame.Surface, activated=False, false_command=None, true_command=None):
        super().__init__(x, y, size, size)
        self.activated = activated
        self.true_command = true_command
        self.false_command = false_command
        false_icon = pygame.transform.scale(false_icon, (self.width, self.height))
        true_icon = pygame.transform.scale(true_icon, (self.width, self.height))
        self.icons = [false_icon, true_icon]

    def render(self, screen: pygame.Surface):
        img_index = 0
        if self.activated:
            img_index = 1
        screen.blit(self.icons[img_index], (self.x, self.y))
        super().render(screen)

    def mouse_input(self, event: pygame.event.Event):
        super().mouse_input(event)
        if self.mouse_inside and self.mouse_clicked:
            self.execute()

    def execute(self):
        if self.activated:
            self.activated = False
            self.exec_false_command()
        else:
            self.activated = True
            self.exec_true_command()

    def exec_false_command(self):
        if self.false_command is not None:
            self.false_command()

    def exec_true_command(self):
        if self.true_command is not None:
            self.true_command()


class ButtonSliderVertical:

    def __init__(self, x, y, length, stroke, color=(255, 255, 255), release_command=None):
        self.x = x
        self.y = y
        self.length = length
        self.stroke = stroke
        self.scroll_pos: float = 0.0
        self.mouse_inside = False
        self.mouse_clicked = False
        self.mouse_focus = False
        self.color = color
        self.release_command = release_command

    def render(self, screen: pygame.Surface):
        # bar
        screen.fill(self.color, (self.x, self.y, self.stroke, self.length))

        # slider
        pygame.draw.circle(screen, self.color, (self.x + self.stroke / 2, self.y + self.length * self.scroll_pos), self.stroke * 2)

    def get_scroll_pos(self):
        return self.scroll_pos

    def set_scroll_pos(self, value: float):
        if value < 0.0:
            self.scroll_pos = 0.0
        elif value > 1.0:
            self.scroll_pos = 1.0
        else:
            self.scroll_pos = value

    def mouse_input(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if (self.x <= mouse_pos[0] <= self.x + self.stroke) and (self.y <= mouse_pos[1] <= self.y + self.length):
            self.mouse_inside = True
        else:
            self.mouse_inside = False

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            self.mouse_clicked = True
            if self.mouse_inside:
                self.mouse_focus = True
        else:
            self.mouse_clicked = False

        if event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
            if self.mouse_focus:
                self.execute()
            self.mouse_focus = False

        if self.mouse_focus:
            if self.y <= mouse_pos[1] <= self.y + self.length:
                self.scroll_pos = (mouse_pos[1] - self.y) / self.length

    def execute(self):
        if self.release_command is not None:
            self.release_command()
