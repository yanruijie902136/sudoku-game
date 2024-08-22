import pygame
from pygame.locals import MOUSEBUTTONUP

from .screen import Screen
from ..utils import Button


class CongratsScreen(Screen):
    """
    The screen showing "CONGRATULATIONS!" when user solved the Sudoku puzzle.
    """

    def __init__(self, game, elapsed_time: str) -> None:
        super().__init__(game)

        self.__new_game_button = Button(
            "NEW GAME", size=(250, 100), right=550, top=550)
        self.__main_menu_button = Button(
            "MAIN MENU", size=(250, 100), left=650, top=550)

        self.__all_sprites = pygame.sprite.RenderPlain(
            self.__new_game_button, self.__main_menu_button
        )

        self.__elapsed_time = elapsed_time

    def display(self) -> None:
        self.game.surface.fill("white")

        font = pygame.font.SysFont("Futura", size=80)
        text = font.render("CONGRATULATIONS!", True, "black")
        text_rect = text.get_rect(center=(600, 330))
        self.game.surface.blit(text, text_rect)

        font = pygame.font.SysFont("Futura", size=50)
        text = font.render(
            f"You solved the puzzle in {self.__elapsed_time}.", True, "black"
        )
        text_rect = text.get_rect(center=(600, 450))
        self.game.surface.blit(text, text_rect)

        self.__all_sprites.update()
        self.__all_sprites.draw(self.game.surface)

        pygame.display.update()

    def handle_events(self) -> None:
        from .select_screen import SelectScreen
        from .title_screen import TitleScreen

        for event in pygame.event.get():
            if self.is_quit_event(event):
                self.game.quit()

            if event.type == MOUSEBUTTONUP:
                if self.__new_game_button.is_hovered():
                    self.game.screen = SelectScreen(self.game)
                    return
                if self.__main_menu_button.is_hovered():
                    self.game.screen = TitleScreen(self.game)
                    return
