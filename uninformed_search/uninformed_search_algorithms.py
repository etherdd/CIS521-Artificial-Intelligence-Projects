import math
import random
from collections import deque

############################################################
# CIS 521: Homework 2
############################################################

student_name = "Yun Dai"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    return math.comb(n**2, n)


def num_placements_one_per_row(n):
    return n**n


def n_queens_valid(board):
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:  # Same column
                return False
            if abs(board[i] - board[j]) == abs(i - j):  # Same diagonal
                return False
    return True


def n_queens_solutions(n):
    def n_queens_helper(board):
        if len(board) == n:
            solutions.append(board[:])
            return

        for col in range(n):
            board.append(col)
            if n_queens_valid(board):
                n_queens_helper(board)
            board.pop()

    solutions = []
    n_queens_helper([])
    return solutions

############################################################
# Section 2: Lights Out
############################################################


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        if row - 1 >= 0:
            self.board[row - 1][col] = not self.board[row - 1][col]
        if col - 1 >= 0:
            self.board[row][col - 1] = not self.board[row][col - 1]
        if col + 1 <= len(self.board[0]) - 1:
            self.board[row][col + 1] = not self.board[row][col + 1]
        if row + 1 <= len(self.board) - 1:
            self.board[row + 1][col] = not self.board[row + 1][col]

    def scramble(self):
        row = len(self.board)
        column = len(self.board[0])
        for i in range(row):
            for j in range(column):
                if random.random() < 0.5:
                    self.perform_move(i, j)

    def is_solved(self):
        row = len(self.board)
        column = len(self.board[0])
        for i in range(row):
            for j in range(column):
                if self.board[i][j] is True:
                    return False
        return True

    def copy(self):
        puzzle = [[cell for cell in row] for row in self.board]
        return LightsOutPuzzle(puzzle)

    def successors(self):
        row = len(self.board)
        column = len(self.board[0])
        for i in range(row):
            for j in range(column):
                new_board = self.copy()
                new_board.perform_move(i, j)
                yield ((i, j), new_board)

    def find_solution(self):
        # initial_state = tuple(tuple(row) for row in self.board)
        if self.is_solved():
            return []

        queue = deque([(self.copy(), [])])
        visited = set()

        while queue:
            current_puzzle, path = queue.popleft()
            visited.add(tuple(
                tuple(row)
                for row
                in current_puzzle.get_board()
                ))
            for move, new_puzzle in current_puzzle.successors():
                new_state = tuple(tuple(row) for row in new_puzzle.get_board())
                if new_state not in visited:
                    if new_puzzle.is_solved():
                        return path + [move]
                    queue.append((new_puzzle, path + [move]))

        return None


def create_puzzle(rows, cols):
    puzzle = [[False for _ in range(cols)] for _ in range(rows)]
    return LightsOutPuzzle(puzzle)


############################################################
# Section 3: Linear Disk Movement
############################################################


def solve_identical_disks(length, n):
    initial_state = tuple(1 if i < n else 0 for i in range(length))
    goal_state = tuple(0 if i < length - n else 1 for i in range(length))

    if initial_state == goal_state:
        return []

    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        visited.add(current_state)
        for i in range(length):
            if current_state[i] == 1:
                if i + 1 < length and current_state[i + 1] == 0:
                    new_state = list(current_state)
                    new_state[i], new_state[i+1] = 0, 1
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        if new_state == goal_state:
                            return path + [(i, i + 1)]
                        queue.append((new_state, path + [(i, i + 1)]))

                if (i + 2 < length
                        and current_state[i + 1] == 1
                        and current_state[i + 2] == 0):
                    new_state = list(current_state)
                    new_state[i], new_state[i + 2] = 0, 1
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        if new_state == goal_state:
                            return path + [(i, i + 2)]
                        queue.append((new_state, path + [(i, i + 2)]))

    return []


def solve_distinct_disks(length, n):
    initial_state = tuple(i + 1 if i < n else 0 for i in range(length))
    goal_state = tuple(
        0 if i < length - n
        else length - i
        for i in range(length))
    if initial_state == goal_state:
        return []

    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        visited.add(current_state)

        for i in range(length):
            if current_state[i] != 0:
                if i + 1 < length and current_state[i + 1] == 0:
                    new_state = list(current_state)
                    new_state[i], new_state[i + 1] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        if new_state == goal_state:
                            return path + [(i, i + 1)]
                        queue.append((new_state, path + [(i, i + 1)]))

                if i - 1 >= 0 and current_state[i - 1] == 0:
                    new_state = list(current_state)
                    new_state[i], new_state[i - 1] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        if new_state == goal_state:
                            return path + [(i, i - 1)]
                        queue.append((new_state, path + [(i, i - 1)]))

                if (i + 2 < length
                        and current_state[i + 1] != 0
                        and current_state[i + 2] == 0):
                    new_state = list(current_state)
                    new_state[i], new_state[i + 2] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        if new_state == goal_state:
                            return path + [(i, i + 2)]
                        queue.append((new_state, path + [(i, i + 2)]))

                if (i - 2 >= 0
                        and current_state[i - 1] != 0
                        and current_state[i - 2] == 0):
                    new_state = list(current_state)
                    new_state[i], new_state[i - 2] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        if new_state == goal_state:
                            return path + [(i, i - 2)]
                        queue.append((new_state, path + [(i, i - 2)]))
    return []

############################################################
# Section 4: Feedback
############################################################


feedback_question_1 = """
6 hrs
"""

feedback_question_2 = """
In BFS and DFS, when should I check the result and
when should I add the stated to visited.
In solve_distinct_disks, it is easy to forget that a disk can move backwords
"""

feedback_question_3 = """
the GUI interface, it makes the assignment way too fun
"""
