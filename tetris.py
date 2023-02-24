import pygame
import game_state
import score_utils
from menu import MenuState
from in_game import InGameState
from scoreboard import ScoreBoardState
from profile import ProfileState, ProfileEditShortcutState
from customize import CustomizeState
from animated_background import AnimatedBackground


pygame.init()
if not pygame.font.get_init():
    pygame.font.init()

screen = pygame.display.set_mode((576, 760))
pygame.display.set_caption("Tetris")
pygame.display.set_icon(pygame.image.load("res/icon.png"))

game_state.state = 0
state = MenuState()

game_state.profile_name = score_utils.get_last_profile()
game_state.second_profile_name = score_utils.get_last_second_profile()

running = True

animated_background = AnimatedBackground()

while running:

    # Update state
    if game_state.update_pending:
        if game_state.load_custom_ingame:
            state = InGameState(game_state.gamemode_type)
            game_state.load_custom_ingame = False
        elif game_state.state == game_state.MENU:
            state = MenuState()
        elif game_state.state == game_state.INGAME:
            state = InGameState()
        elif game_state.state == game_state.PROFILE:
            state = ProfileState()
        elif game_state.state == game_state.SCOREBOARD:
            state = ScoreBoardState()
        elif game_state.state == game_state.CUSTOMIZE:
            state = CustomizeState()
        elif game_state.state == game_state.PROFILE_SHORTCUT_P1:
            state = ProfileEditShortcutState()
        elif game_state.state == game_state.PROFILE_SHORTCUT_P2:
            state = ProfileEditShortcutState(second_profile=True)
        else:
            print("Invalid state id:", game_state.state)
        game_state.update_pending = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        state.input(event)

    state.update()
    animated_background.update()

    screen.fill((30, 30, 30))
    animated_background.render(screen)

    state.render(screen)

    pygame.display.flip()
