from typing import Optional

import pygame
from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_BACKSPACE,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_UP,
)

from .sudoku import Sudoku


CELL_SIZE = 70
GRID_SIZE = CELL_SIZE * 9
MARGIN_SIZE = (900 - GRID_SIZE) / 2

EDIT_KEYS = [K_BACKSPACE, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]


class SudokuGuiWrapper(pygame.sprite.Sprite):
    """
    Display a Sudoku puzzle on the monitor. The cell selected by user (if any)
    is highlighted. The other cells belonging to the same group as the selected
    cell are also highlighted but with a different color.
    """
    def __init__(self, sudoku: Sudoku, **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)

        # A subclass of Sprite should assign `image` and `rect` attributes.
        self.image = pygame.Surface((900, 900))
        self.rect = self.image.get_rect()
        for key, value in kwargs.items():
            setattr(self.rect, key, value)

        self.__cell_rects = [
            [
                pygame.Rect(
                    MARGIN_SIZE + CELL_SIZE * col,
                    MARGIN_SIZE + CELL_SIZE * row,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                for col in range(9)
            ]
            for row in range(9)
        ]
        self.__sudoku = sudoku
        self.__pos: Optional[tuple[int, int]] = None   # The selected cell position.

        self.font = pygame.font.SysFont("Futura", size=30)

    def update(self) -> None:
        self.image.fill("white")

        # Draw the cell rects.
        for row, row_of_cell_rects in enumerate(self.__cell_rects):
            for col, cell_rect in enumerate(row_of_cell_rects):
                pygame.draw.rect(self.image, self.__choose_cell_color(row, col), cell_rect)
                # Draw the digit text.
                if (digit := self.sudoku.get((row, col))) is None:
                    continue
                text = self.font.render(str(digit), True, self.__choose_digit_color(row, col))
                text_rect = text.get_rect(center=cell_rect.center)
                self.image.blit(text, text_rect)

        # Draw the horizontal and vertical lines.
        start, end = MARGIN_SIZE, MARGIN_SIZE + GRID_SIZE
        for i in range(10):
            if i % 3 == 0:
                continue
            stop = MARGIN_SIZE + CELL_SIZE * i
            pygame.draw.line(self.image, "gray", (start, stop), (end, stop), width=3)
            pygame.draw.line(self.image, "gray", (stop, start), (stop, end), width=3)
        for i in [0, 3, 6, 9]:
            stop = MARGIN_SIZE + CELL_SIZE * i
            pygame.draw.line(self.image, "black", (start, stop), (end, stop), width=3)
            pygame.draw.line(self.image, "black", (stop, start), (stop, end), width=3)

    def handle_mouse_event(self) -> None:
        """
        Move the selected position based on where user clicked.
        """
        mouse_pos = pygame.mouse.get_pos()
        for row, row_of_cell_rects in enumerate(self.__cell_rects):
            for col, cell_rect in enumerate(row_of_cell_rects):
                if cell_rect.collidepoint(mouse_pos):
                    self.__pos = (row, col)
                    return
        self.__pos = None

    def handle_key_event(self, key: int) -> None:
        """
        Based on which key user pressed, move the selected position or set digit inside the selected cell.
        """
        if self.__pos is None:
            return

        try:
            index = EDIT_KEYS.index(key)
            self.sudoku.set(self.__pos, digit=(None if index == 0 else index))
            return
        except:
            pass

        row, col = self.__pos
        if key == K_UP:
            row = (row - 1) % 9
        elif key == K_DOWN:
            row = (row + 1) % 9
        elif key == K_LEFT:
            col = (col - 1) % 9
        elif key == K_RIGHT:
            col = (col + 1) % 9
        self.__pos = row, col

    def __choose_cell_color(self, row: int, col: int) -> str:
        """
        Choose the color of a cell.
        """
        if self.__pos is None:
            return "white"
        if self.__pos == (row, col):
            return "azure4"

        selected_digit = self.sudoku.get(self.__pos)
        if self.sudoku.get((row, col)) == selected_digit and selected_digit is not None:
            return "azure3"
        if not self.sudoku.is_same_group((row, col), self.__pos):
            return "white"
        return "azure1"

    def __choose_digit_color(self, row: int, col: int) -> str:
        """
        Choose the color of a digit inside a cell.
        """
        if self.sudoku.is_clue((row, col)):
            return "black"
        return "blue" if self.sudoku.has_valid_digit((row, col)) else "red"

    @property
    def sudoku(self) -> Sudoku:
        """
        The current Sudoku puzzle being displayed. Setting this property also
        resets the selected cell position.
        """
        return self.__sudoku

    @sudoku.setter
    def sudoku(self, new_sudoku: Sudoku) -> Sudoku:
        self.__sudoku = new_sudoku
        self.__pos = None
