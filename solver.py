"""
Alson Lee
Date: 06/03/24

The solver module contains the solving algorithms for an m,n,k-game.
"""

import board
import copy

"""
Solver class which implements a recursive solving algorithm for an m,n,k-game.
"""
class Solver:
    # TODO: Do not solve symmetric rotations and reflections of the same game.

    def __init__(self, default_board):
        self.node_count = 0
        self.default_board = default_board
        self.score_each = None
        if self.score_each is None:
            self.score_each = [[0 for _ in range(self.default_board.M)]
                               for _ in range(self.default_board.N)]
        self.mem_table = {}

    def negamax(self, board_inst: board.Board, alpha: int, beta: int) -> int:        
        """
        Recursively solves a move with the negamax algorithm with alpha-beta pruning.
        Alpha represents the min score for the maximising player (current player).
        Beta represents the max score for the minimising player (other player).
        As the algorithm searches, it keeps track of a score window [alpha, beta].

        E.g. the algo finds a score of 10 for P1, hence for any further searches there is no 
        need to explore scores >10 as the goal is to maximise the score of P1. 
        Moves are assigned a score according to:
        - 0 for a draw
        - >0 if the current player can win no matter what (the faster the win, the higher the score)
        - <0 if the other player can win no matter what (the faster the loss, the lower the score)
        :param board_inst: the board instance being solved
        :param alpha:          the min score for the maximising player (current player)
        :param beta:           the max score for the minimising player (other player)
        :return:               the score for the board instance
        """
        # Increment counter of nodes explored.
        self.node_count += 1

        # First, check if there are no moves available i.e. draw.
        if board_inst.get_num_moves() == board_inst.M * board_inst.N:
            return 0

        # Second, check if the current player can win the next move
        for move in range(board_inst.M * board_inst.N):
            if (board_inst.is_valid_move(move)
                    and board_inst.is_winning_move(move)):
                # If the current player can win, return the score proportional to the moves it takes
                score = (board_inst.M * board_inst.N - board_inst.get_num_moves() + 1) // 2
                return score

        # The upper bound of beta should not exceed the score limited by the board.
        upper_bound = (board_inst.M * board_inst.N - board_inst.get_num_moves() + 1) // 2
        
        # Check if there is a memo for the current solve.
        # memo = self.mem_table.get(board_inst.key())
        # if memo:
        #     upper_bound = memo + board_inst.min_score - 1

        if beta > upper_bound:
            beta = upper_bound
            # If alpha has converged to beta, return score.
            if alpha >= beta:
                return beta

        # Last, check all possible next moves and return the best one
        for move in range(board_inst.M * board_inst.N):
            
            # If valid, try this move
            if board_inst.is_valid_move(move):  
                check_next_move = copy.deepcopy(board_inst)
                check_next_move.play(move)  # Try the valid move on a copy of the board

                # Recursively solve through the move whilst switching +ve, -ve each time.
                score = -self.negamax(check_next_move, -beta, -alpha)
                if score >= beta:
                    return score
                if score > alpha:
                    alpha = score

        # self.mem_table[board_inst.key()] = alpha - board_inst.min_score + 1

        return alpha

    def solve_score_each(self, board_inst: board.Board):
        """
        Solves all valid moves and returns the score of each of the valid 
        moves in matrix form.
        :param board_inst:     the board instance being solved
        :return:               score matrix of each valid move
        """
        for move in range(board_inst.M * board_inst.N):
            if board_inst.is_valid_move(move):
                check_move = copy.deepcopy(board_inst)
                if check_move.is_winning_move(move):
                    score = (board_inst.M * board_inst.N - board_inst.get_num_moves() + 1) // 2
                    self.set_score_each(board_inst, move, score)
                else:
                    check_move.play(move)
                    self.set_score_each(board_inst, move, -self.solve(check_move))
            else:
                self.set_score_each(board_inst, move, None)

        return self.score_each

    def solve(self, board_inst: board.Board) -> int:
        """
        Solves a move with the negamax algorithm with alpha-beta pruning.
        :param board_inst: the board instance being solved
        :return:               the score of the board instance
        """
        return self.negamax(board_inst, 
                            -(board_inst.M * board_inst.N),
                            board_inst.M * board_inst.N)

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

    def set_score_each(self, board_inst: board.Board, move: int, value: int):
        row = move // board_inst.M
        col = move % board_inst.M 
        
        self.score_each[row][col] = value
