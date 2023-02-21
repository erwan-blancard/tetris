import pygame
import game_state
import score_utils
from menu import MenuState
from in_game import InGameState
from scoreboard import ScoreBoardState
from profile import ProfileState
from customize import CustomizeState


pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

screen = pygame.display.set_mode((512, 760))
pygame.display.set_caption("Tetris")

game_state.state = 0
state = InGameState()

game_state.profile_name = score_utils.get_last_profile()

running = True

while running:

    # Update state
    if game_state.update_pending:
        if game_state.state == game_state.MENU:
            state = MenuState()
        elif game_state.state == game_state.INGAME:
            state = InGameState()
        elif game_state.state == game_state.PROFILE:
            state = ProfileState()
        elif game_state.state == game_state.SCOREBOARD:
            state = ScoreBoardState()
        elif game_state.state == game_state.CUSTOMIZE:
            state = CustomizeState()
        else:
            print("Invalid state id:", game_state.state)
        game_state.update_pending = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        state.input(event)

    state.update()

    screen.fill((0, 0, 0))

    state.render(screen)

    pygame.display.flip()
