from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

if TYPE_CHECKING:
    from ..sudoku_game import SudokuGame


class Screen(ABC):
    """
    Abstract screen class. Each subclass represents a screen being displayed on
    the monitor, such as the title screen or the game over screen.
    """
    def __init__(self, game: "SudokuGame") -> None:
        self._game = game

    @abstractmethod
    def display(self) -> None:
        """
        Display the screen on the game's display surface.
        """
        pass

    @abstractmethod
    def handle_events(self) -> None:
        """
        Handle user inputs such as keyboard or mouse. Depending on user inputs
        this method may change the game's currently displaying screen to a
        different one (state design pattern).
        """
        pass

    def is_quit_event(self, event: pygame.event.Event) -> bool:
        """
        Whether user closes the window or presses Escape.
        """
        return event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)

    @property
    def game(self) -> "SudokuGame":
        """
        The game which this screen belongs to.
        """
        return self._game
