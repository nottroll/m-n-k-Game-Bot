import board
import copy

"""
Class for solver
"""
class Solver:
    def __init__(self):
        self.node_count = 0
        self.score_each = None
        if self.score_each is None:
            self.score_each = [[0 for _ in range(board.M)] 
                               for _ in range(board.N)]

    def negamax(self, board_instance: board.Board) -> int:
        """
        Recursively solves a move with the negamax algorithm. A move is assigned
        a score according to:
        - 0 for a draw
        - >0 if player1 can win no matter what (the faster p1 wins, the higher the score)
        - <0 if player2 can win no matter what (the faster p1 loses, the lower the score)
        :param board_instance:
        :return:
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
                    return (board.M * board.N + 1
                            - board_instance.get_num_moves()) // 2

        best_score = -(board.M * board.N + 1 // 2)

        # Last, check all possible next moves and return the best one
        for y in range(board.N):
            for x in range(board.M):
                if board_instance.is_valid_move((y, x)):  # If valid, try this move
                    check_next_move = copy.deepcopy(board_instance)
                    check_next_move.play((y, x))  # Try this move on copy of board

                    score = -self.negamax(check_next_move)  # Recursion through tree
                    if score > best_score:
                        best_score = score  # Keep the best score in the branch only

        return best_score

    def solve_score_each(self, board_instance: board.Board):
        """

        :param board_instance:
        :return:
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

        :param board_instance:
        :return:
        """
        return self.negamax(board_instance)

    def get_node_count(self) -> int:
        """

        :return:
        """
        return self.node_count
    
    def reset_node_count(self):
        """

        :return:
        """
        self.node_count = 0