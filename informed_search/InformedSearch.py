import random
from queue import PriorityQueue
from itertools import count
import math


############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    if rows < 1 or cols < 1:
        return TilePuzzle([])

    puzzle = []
    for row in range(rows):
        puzzle.append([row * cols + col + 1 for col in range(cols)])
    puzzle[rows - 1][cols - 1] = 0
    return TilePuzzle(puzzle)


class TilePuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, direction):

        # find the index of empty tile
        for row in range(self.rows):
            r_index = -1
            c_index = -1
            if 0 in self.board[row]:
                r_index = row
                c_index = self.board[row].index(0)
                break

        if direction == 'up':
            if r_index == 0:
                return False
            self.board[r_index][c_index] = self.board[r_index - 1][c_index]
            self.board[r_index - 1][c_index] = 0
            return True

        elif direction == 'down':
            if r_index == self.rows - 1:
                return False
            self.board[r_index][c_index] = self.board[r_index + 1][c_index]
            self.board[r_index + 1][c_index] = 0
            return True

        elif direction == 'left':
            if c_index == 0:
                return False
            self.board[r_index][c_index] = self.board[r_index][c_index - 1]
            self.board[r_index][c_index - 1] = 0
            return True

        else:
            if c_index == self.cols - 1:
                return False
            self.board[r_index][c_index] = self.board[r_index][c_index + 1]
            self.board[r_index][c_index + 1] = 0
            return True

    def scramble(self, num_moves):
        seq = ['up', 'down', 'left', 'right']
        for i in range(num_moves):
            self.perform_move(random.choice(seq))

    def is_solved(self):
        if self.board[-1][-1] != 0:
            return False
        final_board = [[cell for cell in row] for row in self.board]
        final_board[-1][-1] = self.cols * self.rows
        index = 0
        for row in range(self.rows):
            for col in range(self.cols):
                index += 1
                if final_board[row][col] != index:
                    return False
        return True

    def copy(self):
        puzzle = [[cell for cell in row] for row in self.board]
        return TilePuzzle(puzzle)

    def successors(self):
        for move in ['up', 'down', 'left', 'right']:
            new_board = self.copy()
            if new_board.perform_move(move):
                yield (move, new_board)

    def iddfs_helper(self, limit, moves):
        if self.is_solved():
            yield moves
            return
        if limit == 0:
            return
        for move, new_board in self.successors():
            yield from new_board.iddfs_helper(limit - 1, moves + [move])

    def find_solutions_iddfs(self):
        depth = 0
        solutions = []
        while True:
            solutions = list(self.iddfs_helper(depth, []))
            if solutions:
                break
            depth += 1

        for solution in solutions:
            yield solution

    def manhattan_distance(self):
        distance = 0
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.board[r][c]
                if value == 0:
                    continue
                target_r = (value - 1) // self.cols
                target_c = (value - 1) % self.cols
                distance += abs(r - target_r) + abs(c - target_c)
        return distance

    def find_solution_a_star(self):
        start_board = self.copy()
        counter = count()
        start_state = (
            start_board.manhattan_distance(),
            next(counter),
            start_board,
            [])
        queue = PriorityQueue()
        queue.put(start_state)
        visited = set()

        while not queue.empty():
            _, _, current_board, path = queue.get()
            current_tuple = tuple(
                tuple(row) for row in current_board.get_board()
                )

            if current_board.is_solved():
                return path

            if current_tuple in visited:
                continue

            visited.add(current_tuple)

            for move, new_board in current_board.successors():
                new_tuple = tuple(tuple(row) for row in new_board.get_board())
                if new_tuple not in visited:
                    new_path = path + [move]
                    cost = len(new_path) + new_board.manhattan_distance()
                    queue.put((cost, next(counter), new_board, new_path))

        return None


############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    def euclidean_distance(point1, point2):
        return math.sqrt(
            (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
            )

    def is_valid_move(point):
        row, col = point
        return (
            0 <= row < len(scene)
            and 0 <= col < len(scene[0])
            and not scene[row][col]
            )

    if not is_valid_move(start) or not is_valid_move(goal):
        return None

    start_point = start
    goal_point = goal

    queue = PriorityQueue()
    counter = count()
    cost_start = euclidean_distance(start_point, goal_point)
    path_cost = 0
    queue.put(
        (cost_start, path_cost, next(counter), start_point, [start_point])
        )
    visited = set()

    while not queue.empty():
        _, path_cost, _, current, path = queue.get()

        if current == goal_point:
            return path

        if current in visited:
            continue

        visited.add(current)

        row, col = current
        for d_row, d_col in [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]:
            neighbor = (row + d_row, col + d_col)
            if is_valid_move(neighbor) and neighbor not in visited:
                new_path = path + [neighbor]
                # calculate the precise path length
                move_cost = (
                    math.sqrt(2)
                    if abs(d_row) == 1 and abs(d_col) == 1
                    else 1
                    )
                new_path_cost = path_cost + move_cost
                cost = new_path_cost + euclidean_distance(neighbor, goal_point)
                queue.put(
                    (cost, new_path_cost, next(counter), neighbor, new_path)
                    )

    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################


def solve_distinct_disks(length, n):
    initial_state = tuple(i + 1 if i < n else 0 for i in range(length))
    goal_state = tuple(
        0 if i < length - n
        else length - i
        for i in range(length))
    if initial_state == goal_state:
        return []

    def heuristic(state):
        # Calculate the heuristic as the sum of
        # Manhattan distances of each disk to its goal position
        # it can be a 2 grid move or 1 grid move,
        # so the total distance should be divided with 1.5
        total_distance = 0
        for i in range(length):
            if state[i] != 0:
                target_position = length - state[i]
                total_distance += abs(target_position - i)
        return total_distance / 1.5

    queue = PriorityQueue()
    counter = count()
    queue.put((0, next(counter), initial_state, []))
    visited = set()

    while not queue.empty():
        _, _, current_state, path = queue.get()

        if current_state == goal_state:
            return path

        if current_state in visited:
            continue

        visited.add(current_state)

        for i in range(length):
            if current_state[i] != 0:
                # Move to the adjacent empty cell
                if i + 1 < length and current_state[i + 1] == 0:
                    new_state = list(current_state)
                    new_state[i], new_state[i + 1] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        new_path = path + [(i, i + 1)]
                        cost = len(new_path) + heuristic(new_state)
                        queue.put((cost, next(counter), new_state, new_path))

                if i - 1 >= 0 and current_state[i - 1] == 0:
                    new_state = list(current_state)
                    new_state[i], new_state[i - 1] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        new_path = path + [(i, i - 1)]
                        cost = len(new_path) + heuristic(new_state)
                        queue.put((cost, next(counter), new_state, new_path))

                # Move to the empty cell two spaces away
                # if there's a disk in between
                if (
                    i + 2 < length
                    and current_state[i + 1] != 0
                    and current_state[i + 2] == 0
                ):
                    new_state = list(current_state)
                    new_state[i], new_state[i + 2] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        new_path = path + [(i, i + 2)]
                        cost = len(new_path) + heuristic(new_state)
                        queue.put((cost, next(counter), new_state, new_path))

                if (
                    i - 2 >= 0
                    and current_state[i - 1] != 0
                    and current_state[i - 2] == 0
                ):
                    new_state = list(current_state)
                    new_state[i], new_state[i - 2] = 0, new_state[i]
                    new_state = tuple(new_state)
                    if new_state not in visited:
                        new_path = path + [(i, i - 2)]
                        cost = len(new_path) + heuristic(new_state)
                        queue.put((cost, next(counter), new_state, new_path))

    return []


############################################################
# Section 4: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 10

feedback_question_2 = """
1. find_solutions_iddfs. It is challenging to code the correct yield
2. Linear Disk Movement. it's challenging to design the heuristic function.
The returned value should be divided by 1.5
because it can be a 2 grid move or 1 grid move.
In this way g(n) will not be overwelmed by h(n)
"""

feedback_question_3 = """
Grid Navigation and Linear Disk Movement.
Adjusting heuristic function and see
how the search result is optimized is so fun.
"""
