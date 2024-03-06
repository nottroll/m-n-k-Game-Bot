"""
Alson Lee
Date: 02/03/24
"""

import board
import copy

"""
Solver class which implements a recursive solving algorithm for an m,n,k-game.
"""
class Solver:
    # TODO: Do not solve symmetric rotations and reflections of the same game.

    def __init__(self):
        self.node_count = 0
        self.score_each = None
        if self.score_each is None:
            self.score_each = [[0 for _ in range(board.M)]
                               for _ in range(board.N)]

    def negamax(self, board_instance: board.Board, alpha: int,
                beta: int) -> int:
        """
        Recursively solves a move with the negamax algorithm with alpha-beta pruning.
        Alpha represents the min score for the maximising player (P1).
        Beta represents the max score for the minimising player (P2).
        As the algorithm searches, it keeps track of a score window [alpha, beta].

        E.g. the algo finds a score of 10 for P1, hence for any further searches there is no 
        need to explore scores >10 as the goal is to maximise the score of P1. 
        Moves are assigned a score according to:
        - 0 for a draw
        - >0 if player1 can win no matter what (the faster p1 wins, the higher the score)
        - <0 if player2 can win no matter what (the faster p1 loses, the lower the score)
        :param board_instance: the board instance being solved
        :param alpha:          the min score for the maximising player (P1)
        :param beta:           the max score for the minimising player (P2)
        :return:               the score for the board instance
        """
        # Increment counter of nodes explored.
        self.node_count += 1

        # First, check if there are no moves available i.e. draw.
        if board_instance.get_num_moves() == board.M * board.N:
            return 0

        # Second, check if the player can win the next move
        for y in range(board.N):
            for x in range(board.M):
                if (board_instance.is_valid_move((y, x))
                        and board_instance.is_winning_move((y, x))):
                    # If the player can win, return the number of moves it takes
                    return (board.M * board.N
                            - board_instance.get_num_moves() + 1) // 2

        # The upper bound of beta should not exceed the score limited by the board.
        upper_bound = (board.M * board.N - board_instance.get_num_moves() - 1) // 2
        if beta > upper_bound:
            beta = upper_bound
            # If alpha has converged to beta, return score.
            if alpha >= beta:
                return beta

        # Last, check all possible next moves and return the best one
        for y in range(board.N):
            for x in range(board.M):
                if board_instance.is_valid_move(
                        (y, x)):  # If valid, try this move
                    check_next_move = copy.deepcopy(board_instance)
                    check_next_move.play(
                        (y, x))  # Try the valid move on copy of board

                    # Recursively solve through the move switching +ve, -ve each time.
                    score = -self.negamax(check_next_move, -beta, -alpha)
                    if score >= beta:
                        return beta
                    if score > alpha:
                        alpha = score

        return alpha

    def solve_score_each(self, board_instance: board.Board):
        """
        Solves all valid moves and returns the score of each of the valid 
        moves in matrix form.
        :param board_instance: the board instance being solved
        :return:               score matrix of each valid move
        """
        for y in range(board.N):
            for x in range(board.M):
                if board_instance.is_valid_move((y, x)):
                    check_move = copy.deepcopy(board_instance)
                    if check_move.is_winning_move((y, x)):
                        self.score_each[y][x] = (board.M * board.N + 1
                                                 - board_instance.get_num_moves()) // 2
                    else:
                        check_move.play((y, x))
                        self.score_each[y][x] = self.solve(check_move)
                else:
                    self.score_each[y][x] = None

        return self.score_each

    def solve(self, board_instance: board.Board) -> int:
        """
        Solves a move with the negamax algorithm with alpha-beta pruning.
        :param board_instance: the board instance being solved
        :return:               the score of the board instance
        """
        return self.negamax(board_instance, 
                            -board.M * board.N // 2,
                            board.M * board.N // 2)

    def get_node_count(self) -> int:
        """
        Returns the number of nodes which have been explored in the solver instance.
        :return: number of nodes which have been explored
        """
        return self.node_count

    def reset_node_count(self):
        """
        Resets the number of nodes which have been explored to 0.
        """
        self.node_count = 0
