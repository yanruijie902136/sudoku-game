import os
import random
from typing import Literal, Optional


CellPos = tuple[int, int]
Difficulty = Literal["easy", "medium", "hard"]


class _Cell:
    """
    A cell in Sudoku puzzle.
    """
    def __init__(self, char: str) -> None:
        self.__digit = None if char == "." else int(char)
        self.__is_clue = (self.__digit is not None)

    @property
    def digit(self) -> Optional[int]:
        """
        The digit inside the cell or `None` if empty. Setting this property will
        have completely no effect if this cell is a clue.
        """
        return self.__digit

    @digit.setter
    def digit(self, new_digit: Optional[int]) -> None:
        if not self.is_clue:
            self.__digit = new_digit

    @property
    def is_clue(self) -> bool:
        """
        Whether this cell is a clue. A cell is a clue if its digit is initially
        given. Its digit cannot be altered.
        """
        return self.__is_clue


class Sudoku:
    """
    Classic 9x9 Sudoku puzzle.
    """
    def __init__(self, difficulty: Difficulty = "easy", filename: Optional[str] = None) -> None:
        """
        Load the puzzle from a file with specified difficulty.
        """
        if filename is None:
            puzzle_dir = f"data/puzzles/{difficulty}"
            filename = os.path.join(puzzle_dir, random.choice(os.listdir(puzzle_dir)))
        with open(filename, mode="r") as fp:
            board = fp.read().splitlines()

        # TODO: Randomly shuffle rows and columns, and decide a random 1-to-1
        # mapping from digits to digits, in order to produce more legal puzzles.

        self.__grid = [[_Cell(char) for char in line] for line in board]

    def get(self, pos: CellPos) -> Optional[int]:
        """
        Get the digit inside a cell.
        """
        row, col = pos
        return self.__grid[row][col].digit

    def set(self, pos: CellPos, digit: Optional[int]) -> None:
        """
        Set the digit inside a cell.
        """
        row, col = pos
        self.__grid[row][col].digit = digit

    def is_clue(self, pos: CellPos) -> bool:
        """
        Whether the cell is a clue.
        """
        row, col = pos
        return self.__grid[row][col].is_clue

    def is_same_group(self, pos1: CellPos, pos2: CellPos) -> bool:
        """
        Whether two cells belong to the same group (row, column or 3x3 box).
        """
        (row1, col1), (row2, col2) = pos1, pos2
        return row1 == row2 or col1 == col2 or (row1//3, col1//3) == (row2//3, col2//3)

    def has_valid_digit(self, pos: CellPos) -> bool:
        """
        Whether the cell contains a digit not seen in other cells of the same
        group (row, column, or 3x3 box). An empty cell is considered valid.
        """
        if (digit := self.get(pos)) is None:
            return True

        for npos in (
            self.__row_pos_list(pos) + \
            self.__col_pos_list(pos) + \
            self.__box_pos_list(pos)
        ):
            if npos != pos and self.get(npos) == digit:
                return False
        return True

    def is_solved(self) -> bool:
        """
        Whether the puzzle has been solved.
        """
        def has_9_digits(digits: set[Optional[int]]) -> bool:
            return None not in digits and len(digits) == 9

        ROWS = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        COLS = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        for pos in zip(ROWS, COLS):
            row_digits = set(self.get(npos) for npos in self.__row_pos_list(pos))
            col_digits = set(self.get(npos) for npos in self.__col_pos_list(pos))
            box_digits = set(self.get(npos) for npos in self.__box_pos_list(pos))
            if not (
                has_9_digits(row_digits) and has_9_digits(col_digits) and has_9_digits(box_digits)
            ):
                return False
        return True

    def reset(self) -> None:
        """
        Reset the puzzle.
        """
        for row in range(9):
            for col in range(9):
                self.set((row, col), digit=None)

    def __row_pos_list(self, pos: CellPos) -> list[CellPos]:
        """
        Get the positions of cells within the same row as the given cell.
        """
        row, _ = pos
        return [(row, i) for i in range(9)]

    def __col_pos_list(self, pos: CellPos) -> list[CellPos]:
        """
        Get the positions of cells within the same column as the given cell.
        """
        _, col = pos
        return [(i, col) for i in range(9)]

    def __box_pos_list(self, pos: CellPos) -> list[CellPos]:
        """
        Get the positions of cells within the same 3x3 box as the given cell.
        """
        row, col = pos
        return [(row//3*3+i, col//3*3+j) for i in range(3) for j in range(3)]
