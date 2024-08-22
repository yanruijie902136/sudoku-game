import pygame
from pygame.locals import MOUSEBUTTONUP

from .screen import Screen
from ..utils import Button


class TitleScreen(Screen):
    """
    The title screen shown at the start of the game.
    """

    def __init__(self, game) -> None:
        super().__init__(game)

        self.__new_game_button = Button(
            "NEW GAME", size=(250, 100), right=550, top=550)
        self.__quit_button = Button("QUIT", size=(
            250, 100), fg_color="red", left=650, top=550)

        self.__all_sprites = pygame.sprite.RenderPlain(
            self.__new_game_button, self.__quit_button
        )

    def display(self) -> None:
        self.game.surface.fill("white")

        font = pygame.font.SysFont("Futura", size=70)
        text = font.render("SUDOKU", True, "black")
        text_rect = text.get_rect(center=(600, 400))
        self.game.surface.blit(text, text_rect)

        self.__all_sprites.update()
        self.__all_sprites.draw(self.game.surface)

        pygame.display.update()

    def handle_events(self) -> None:
        from .select_screen import SelectScreen

        for event in pygame.event.get():
            if self.is_quit_event(event):
                self.game.quit()

            if event.type == MOUSEBUTTONUP:
                if self.__new_game_button.is_hovered():
                    self.game.screen = SelectScreen(self.game)
                    return
                if self.__quit_button.is_hovered():
                    self.game.quit()
