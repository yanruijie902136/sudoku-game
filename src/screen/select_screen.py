import pygame
from pygame.locals import MOUSEBUTTONUP

from .screen import Screen
from ..utils import Button


class SelectScreen(Screen):
    """
    The screen where user select difficulty of a new Sudoku puzzle.
    """

    def __init__(self, game) -> None:
        super().__init__(game)

        self.__easy_button = Button("EASY", size=(200, 100), right=450, top=550)
        self.__medium_button = Button("MEDIUM", size=(200, 100), centerx=600, top=550)
        self.__hard_button = Button("HARD", size=(200, 100), left=750, top=550)

        self.__all_sprites = pygame.sprite.RenderPlain(
            self.__easy_button, self.__medium_button, self.__hard_button
        )

    def display(self) -> None:
        self.game.surface.fill("white")

        font = pygame.font.SysFont("Futura", size=80)
        text = font.render("DIFFICULTY", True, "black")
        text_rect = text.get_rect(center=(600, 400))
        self.game.surface.blit(text, text_rect)

        self.__all_sprites.update()
        self.__all_sprites.draw(self.game.surface)

        pygame.display.update()

    def handle_events(self) -> None:
        from .playing_screen import PlayingScreen

        for event in pygame.event.get():
            if self.is_quit_event(event):
                self.game.quit()

            if event.type == MOUSEBUTTONUP:
                if self.__easy_button.is_hovered():
                    self.game.screen = PlayingScreen(self.game, difficulty="easy")
                    return
                if self.__medium_button.is_hovered():
                    self.game.screen = PlayingScreen(self.game, difficulty="medium")
                    return
                if self.__hard_button.is_hovered():
                    self.game.screen = PlayingScreen(self.game, difficulty="hard")
                    return
