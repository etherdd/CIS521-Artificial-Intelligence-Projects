
import collections
import copy
import itertools
import random
import math

# update the comments
def sudoku_cells():
    return [(r, c) for r in range(9) for c in range(9)]


def sudoku_arcs():
    arcs = set()
    cells = sudoku_cells()

    for r in range(9):
        for c in range(9):
            cell = (r, c)

            # to check row constraints
            for col in range(9):
                if col != c:
                    arcs.add((cell, (r, col)))
                    arcs.add(((r, col), cell))

            # to check column constraints
            for row in range(9):
                if row != r:
                    arcs.add((cell, (row, c)))
                    arcs.add(((row, c), cell))

            start_row, start_col = 3 * (r // 3), 3 * (c // 3)
            for i in range(3):
                for j in range(3):
                    neighbor = (start_row + i, start_col + j)
                    if neighbor != cell:
                        arcs.add((cell, neighbor))
                        arcs.add((neighbor, cell))

    return list(arcs)

'''
something not necessary
'''
def read_board(path):
    board = {}
    with open(path, 'r') as f:
        lines = f.readlines()
        for r, line in enumerate(lines):
            for c, char in enumerate(line.strip()):
                if char == '*':
                    board[(r, c)] = set(range(1, 10))
                else:
                    board[(r, c)] = {int(char)}
    return board


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        removed = False
        values1 = self.board[cell1]
        values2 = self.board[cell2]

        inconsistent_values = {
            v1 for v1 in values1 if not any(v2 != v1 for v2 in values2)
            }

        if inconsistent_values:
            self.board[cell1] -= inconsistent_values
            removed = True

        return removed

    def infer_ac3(self):
        queue = list(self.ARCS)
        while queue:
            (cell1, cell2) = queue.pop(0)
            if self.remove_inconsistent_values(cell1, cell2):
                for cell in self.CELLS:
                    if (
                            cell != cell1
                            and cell != cell2
                            and (cell, cell1) in self.ARCS
                            ):
                        queue.append((cell, cell1))

    def infer_improved(self):
        self.infer_ac3()

        while True:
            found_new_value = False

            for cell in self.CELLS:
                if len(self.board[cell]) == 1:
                    continue
                row, col = cell

                row_values = [
                    self.board[(row, c)] for c in range(9)
                    if (row, c) != cell
                    ]
                row_values_flat = set().union(*row_values)
                unique_row_values = self.board[cell] - row_values_flat
                if len(unique_row_values) == 1:
                    self.board[cell] = unique_row_values
                    found_new_value = True

                col_values = [
                    self.board[(r, col)] for r in range(9)
                    if (r, col) != cell
                    ]
                col_values_flat = set().union(*col_values)
                unique_col_values = self.board[cell] - col_values_flat
                if len(unique_col_values) == 1:
                    self.board[cell] = unique_col_values
                    found_new_value = True

                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                block_values = [
                    self.board[(r, c)] for r in range(start_row, start_row + 3)
                    for c in range(start_col, start_col + 3) if (r, c) != cell
                    ]
                block_values_flat = set().union(*block_values)
                unique_block_values = self.board[cell] - block_values_flat
                if len(unique_block_values) == 1:
                    self.board[cell] = unique_block_values
                    found_new_value = True

            if found_new_value:
                # Re-run AC-3 if we found any new value
                self.infer_ac3()
            else:
 
                break

feedback_question_2 = """
Understanding AC-3 and backreackng is difficult.
"""

    def infer_with_guessing(self):
        self.infer_improved()

        if self.is_solved():
            return True

        cell = min(
            (cell for cell in self.CELLS if len(self.board[cell]) > 1),
            key=lambda x: len(self.board[x]),
            default=None
            )

        if cell is None:
            return False  # No solution found

        original_values = self.board[cell].copy()

        for value in original_values:
            self.board[cell] = {value}
            board_backup = {
                cell: self.board[cell].copy() for cell in self.CELLS
                }

            self.infer_improved()

            if self.infer_with_guessing():
                return True

            self.board = board_backup

        return False

    def is_solved(self):
        return all(len(values) == 1 for values in self.board.values())


feedback_question_2 = """
Understanding AC-3 and backreackng is difficult.
"""

feedback_question_2 = """
Understanding AC-3 and backreackng is difficult.
"""

feedback_question_3 = """
how the algothrisms based on each other
"""
