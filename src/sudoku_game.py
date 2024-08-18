import sys
from typing import NoReturn

import pygame

from .screen import Screen


class SudokuGame:
    """
    A simple Sudoku game with graphical interface.
    """
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(title="Sudoku Game")

        self.__surface = pygame.display.set_mode(size=(1200, 900))

    def start(self) -> NoReturn:
        """
        Start executing the game loop.
        """
        from .screen import TitleScreen

        self.__screen = TitleScreen(game=self)
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.__screen.handle_events()
            self.__screen.display()

    def quit(self) -> NoReturn:
        """
        Close the game. This terminates the process with exit code 0.
        """
        sys.exit(0)

    @property
    def surface(self) -> pygame.Surface:
        """
        The game's display surface. Changes made to this surface will appear on
        the monitor.
        """
        return self.__surface

    @property
    def screen(self) -> Screen:
        """
        The screen currently being displayed. This property should only be set
        by `Screen` subclasses (state design pattern).
        """
        return self.__screen

    @screen.setter
    def screen(self, new_screen: Screen) -> None:
        self.__screen = new_screen
