
import collections
import copy
import itertools
import random
import math




def create_dominoes_game(rows, cols):
    board = [[False for _ in range(cols)] for _ in range(rows)]
    return DominoesGame(board)


class DominoesGame(object):

    def __init__(self, board):
        """
        Initializes the DominoesGame with the given board.

        :param board: A two-dimensional list of Boolean values
        where True represents a filled square
        and False represents an empty square.
        """
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0

    def get_board(self):
        """
        Returns the current state of the board.
        :return: The board as a two-dimensional list of Boolean values.
        """
        return self.board

    def reset(self):
        """
        Resets all of the internal board's squares
        to the empty state (False).
        """
        self.board = [
                [False for _ in range(self.cols)]
                for _ in range(self.rows)
            ]

    def is_legal_move(self, row, col, vertical):
        """
        Checks if the move is legal on the current board.

        :param row: The row index of the starting square.
        :param col: The column index of the starting square.
        :param vertical: A boolean indicating
        if the domino is placed vertically.
        :return: True if the move is legal, False otherwise.
        """
        if vertical:
            # Check if the domino would be out of bounds vertically
            if row + 1 >= self.rows:
                return False
            # Check if the two squares are already filled
            if self.board[row][col] or self.board[row + 1][col]:
                return False
        else:
            # Check if the domino would be out of bounds horizontally
            if col + 1 >= self.cols:
                return False
            # Check if the two squares are already filled
            if self.board[row][col] or self.board[row][col + 1]:
                return False
        return True

    def legal_moves(self, vertical):
        """
        Generates all legal moves for the given orientation.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        """
        Updates the board according to
        the given position and orientation

        :param row col: the given position
        :param vertical: A boolean indicating the current player.
        """
        if vertical:
            self.board[row][col], self.board[row + 1][col] = True, True
        else:
            self.board[row][col], self.board[row][col + 1] = True, True

    def game_over(self, vertical):
        """
        Returns whether the current player is unable to
        place any dominoes.

        :param vertical: A boolean indicating
        if the current player places vertical dominoes.
        :return: True if the player cannot place any dominoes,
        False otherwise.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i, j, vertical):
                    return False
        return True
############################################################
# CIS 521: Homework 4
############################################################

student_name = "Yun Dai"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Dominoes Game
############################################################
    def copy(self):
        """
        :return: A new DominoesGame object with a copied board.
        """
        return DominoesGame([i[:] for i in self.board])

    def successors(self, vertical):
        """
        Uses legal_moves to generate all legal moves for
        the given orientation.
        For each legal move, creates a new game state
        by copying the current game and performing the move.
        Yields a tuple containing the move and the new game state.
        """
        for i, j in self.legal_moves(vertical):
            new_board = self.copy()
            new_board.perform_move(i, j, vertical)
            yield ((i, j), new_board)

    def get_random_move(self, vertical):
        legal_moves = list(self.legal_moves(vertical))
        return random.choice(legal_moves)

    def utility(self, vertical):
        """
        Evaluation function of the board
        Compute the number of moves available to the current player,
        then subtract the number of moves available to the opponent.
        """
        return (
            len(list(self.legal_moves(vertical)))
            - len(list(self.legal_moves(not vertical)))
            )
############################################################
# CIS 521: Homework 4
############################################################

student_name = "Yun Dai"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Dominoes Game
############################################################
    def get_best_move(self, vertical, limit):
        """
        Implementation of the alpha-beta search
        with limit moves (the total moves for player and the opponent)
        """
        # counter for leaf nodes
        count = 0

        def max_value(state, alpha, beta, depth):
            nonlocal count
            # check if reach the leaf:
            # 1 current player cannot move. 2 depth is 0.
            if state.game_over(vertical) or depth == 0:
                count += 1
                return state.utility(vertical), None
            v, best_move = -float('inf'), None
            for move, new_state in state.successors(vertical):
                v2, _ = min_value(new_state, alpha, beta, depth - 1)
                if v2 > v:
                    v, best_move = v2, move
                alpha = max(alpha, v)
                if v >= beta:
                    break
                # print('max', v2, move, alpha, beta)
            return v, best_move

        def min_value(state, alpha, beta, depth):
            nonlocal count
            # check if reach the leaf:
            # 1 opppnent cannot move. 2 depth is 0.
            if state.game_over(not vertical) or depth == 0:
                count += 1
                return state.utility(vertical), None
            v, best_move = float('inf'), None
            for move, new_state in state.successors(not vertical):
                v2, _ = max_value(new_state, alpha, beta, depth - 1)
                if v2 < v:
                    v, best_move = v2, move
                beta = min(beta, v)
                if v <= alpha:
                    break
                # print('min', v2, move, alpha, beta)
            return v, best_move

        value, move = max_value(self, -float('inf'), float('inf'), limit)
        return move, value, count

############################################################
# Section 2: Feedback
############################################################

############################################################
# CIS 521: Homework 4
############################################################

student_name = "Yun Dai"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Dominoes Game
############################################################
feedback_question_3 = """
The implementation of alpha beta algorithm
"""
