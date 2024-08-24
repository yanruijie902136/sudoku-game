import pygame
from pygame.locals import KEYUP, MOUSEBUTTONUP

from .screen import Screen
from ..sudoku import Difficulty, Sudoku, SudokuGuiWrapper
from ..utils import Button, Timer


CENTERX = 765 + (1200-765)/2


class PlayingScreen(Screen):
    """
    The screen shown when user is solving a puzzle.
    """

    def __init__(self, game, difficulty: Difficulty) -> None:
        super().__init__(game)

        self.__sudoku_wrapper = SudokuGuiWrapper(Sudoku(difficulty=difficulty), topleft=(0, 0))
        self.__timer = Timer(size=(250, 100), top=135, centerx=CENTERX)

        self.__undo_button = Button("UNDO", size=(110, 100), bottom=465, right=CENTERX-15)
        self.__redo_button = Button("REDO", size=(110, 100), bottom=465, left=CENTERX+15)

        self.__reset_button = Button(
            "RESET", size=(250, 100), fg_color="red", bottom=615, centerx=CENTERX
        )
        self.__main_menu_button = Button("MAIN MENU", size=(250, 100), bottom=765, centerx=CENTERX)

        self.__all_sprites = pygame.sprite.RenderPlain(
            self.__sudoku_wrapper,
            self.__timer,
            self.__undo_button,
            self.__redo_button,
            self.__reset_button,
            self.__main_menu_button,
        )

    def display(self) -> None:
        self.game.surface.fill("white")

        self.__all_sprites.update()
        self.__all_sprites.draw(self.game.surface)

        pygame.display.update()

    def handle_events(self) -> None:
        from .congrats_screen import CongratsScreen
        from .title_screen import TitleScreen

        for event in pygame.event.get():
            if self.is_quit_event(event):
                self.game.quit()

            if event.type == KEYUP:
                self.__sudoku_wrapper.handle_key_event(event.key)
                if self.__sudoku_wrapper.sudoku.is_solved():
                    self.game.screen = CongratsScreen(
                        self.game, self.__timer.get_elapsed_time())
                    return

            if event.type == MOUSEBUTTONUP:
                if self.__reset_button.is_hovered():
                    self.__sudoku_wrapper.reset()
                    self.__timer.reset()
                elif self.__undo_button.is_hovered():
                    self.__sudoku_wrapper.undo()
                elif self.__redo_button.is_hovered():
                    self.__sudoku_wrapper.redo()
                elif self.__main_menu_button.is_hovered():
                    self.game.screen = TitleScreen(self.game)
                    return
                else:
                    self.__sudoku_wrapper.handle_mouse_event()
