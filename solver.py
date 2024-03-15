"""
Alson Lee
Date: 15/03/24

The solver module contains the solving algorithms for an m,n,k-game.
"""

import numpy as np
# import multiprocessing as mp
# print(f'CPU cores available: {mp.cpu_count()}')

import board
import copy

"""
Solver class which implements a recursive solving algorithm for an m,n,k-game.
"""
class Solver:

    def __init__(self, default_board):
        self.node_count = 0
        self.default_board = default_board

        self.score_each = None
        if self.score_each is None:
            self.score_each = [[0 for _ in range(self.default_board.M)]
                               for _ in range(self.default_board.N)]
        
        self.search_order = []
        if not self.search_order:
            self.search_order = self.generate_search_order()

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
        - 0 if at best the move can draw the game.
        - >0 if the current player can win no matter what (the faster the win, the higher the score)
        - <0 if the other player can win no matter what (the faster the loss, the lower the score)
        
        :param board_inst: the board instance being solved
        :param alpha:      the min score for the maximising player (current player)
        :param beta:       the max score for the minimising player (other player)
        :return:           the score for the board instance
        """
        # print(f'key{board_inst.key():>6}  a{alpha:>3}  b{beta:>3}')

        # Increment counter of nodes explored.
        # self.node_count += 1
        # if self.node_count % 10000 == 0: print(f'Nodes searched: {self.node_count}')

        # First, check if there are no moves available i.e. draw.
        if board_inst.get_num_moves() == board_inst.M * board_inst.N:
            return 0

        # Second, check if the current player can win the next move
        for i in range(board_inst.M * board_inst.N):
            move = np.uint(self.search_order[i])
            if (board_inst.is_valid_move(move)
                    and board_inst.is_winning_move(move)):
                # If the current player can win, return the score proportional to the moves it takes
                score = (board_inst.M * board_inst.N - board_inst.get_num_moves() + 1) // 2
                return score

        # The upper bound of beta should not exceed the score limited by the board.
        upper_bound = (board_inst.M * board_inst.N - board_inst.get_num_moves() - 1) // 2
        
        # Check if there is a memo for the current solve.
        # memo = self.mem_table.get(board_inst.key())
        # if memo:
            # print(f'   HIT {board_inst.key()}')
            # upper_bound = memo

        if beta > upper_bound:
            beta = upper_bound
            # If alpha has converged to beta, return score.
            if alpha >= beta:
                return beta
            
        # TODO: Do not solve symmetric rotations and reflections of the same game.

        # Last, check all possible next moves and return the best one
        for i in range(board_inst.M * board_inst.N):
            move = np.uint(self.search_order[i])
            # If valid, try this move
            if board_inst.is_valid_move(move):  
                check_next_move = copy.deepcopy(board_inst)
                check_next_move.play(move)  # Try the valid move on a copy of the board

                # Recursively solve through the move whilst switching +ve, -ve each time.
                score = -self.negamax(check_next_move, -beta, -alpha)
                
                # Return score if a better move is found
                if score >= beta:
                    return score
                
                if score > alpha:
                    alpha = score

        # self.mem_table[board_inst.key()] = alpha

        return alpha

    def solve_score_each(self, board_inst: board.Board):
        """
        Solves all valid moves and returns the score of each of the valid 
        moves in matrix form.
        :param board_inst:     the board instance being solved
        :return:               score matrix of each valid move
        """
        for i in range(board_inst.M * board_inst.N):
            move = np.uint(self.search_order[i])
            if board_inst.is_valid_move(move):
                check_move = copy.deepcopy(board_inst)
                if check_move.is_winning_move(move):
                    score = (board_inst.M * board_inst.N - board_inst.get_num_moves() + 1) // 2
                    self.set_score_each(move, score)
                else:
                    check_move.play(move)
                    self.set_score_each(move, -self.solve(check_move))
            else:
                self.set_score_each(move, None)

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
         number of nodes which have been explored
        """
        return self.node_count

    def reset_node_count(self):
        """
        Resets the number of nodes which have been explored to 0.
        """
        self.node_count = 0

    def set_score_each(self, move: np.uint, value: int):
        row = int(move) // self.default_board.M
        col = int(move) % self.default_board.M 
        
        self.score_each[row][col] = value

    def generate_search_order(self) -> list:
        """
        Generate the search order starting from the centre and spiralling 
        outwards clockwise. The theory is that moves played near the centre 
        have more impactful branches which will create more opportunities for 
        alpha-beta pruning.
        :return: the search order generated
        """
        rows, cols = self.default_board.N, self.default_board.M
        board = [[r * cols + c for c in range(cols)] for r in range(rows)]              

        top, bottom, left, right = 0, rows-1, 0, cols-1
        result = []
        
        while len(result) < rows * cols:
            for i in range(left, right+1):
                result.append(board[top][i])
            top += 1
            
            for i in range(top, bottom+1):
                result.append(board[i][right])
            right -= 1
            
            if top <= bottom:
                for i in range(right, left-1, -1):
                    result.append(board[bottom][i])
                bottom -= 1
            
            if left <= right:
                for i in range(bottom, top-1, -1):
                    result.append(board[i][left])
                left += 1

        return list(reversed(result))
