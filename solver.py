import board
import copy


class Solver:
    def __init__(self):
        self.node_count = 0
        self.scores = None
        # self.curr_move = curr_move

    def set_scores(self, move, score):
        b = board.Board()
        if self.scores is None:
            self.scores = [[0 for _ in range(b.WIDTH)] for _ in range(b.HEIGHT)]
        else:
            y, x = move
            self.scores[y][x] = score

    def negamax(self, board: board.Board) -> int:
        """
        Recursively solves a move with the negamax algorithm. A move is assigned
        a score according to:
        - 0 for a draw
        - >0 if player1 can win (the faster p1 wins, the higher the score)
        - <0 if player2 can win (the faster p1 loses, the lower the score)
        :param board:
        :return:
        """
        # Increment counter of nodes explored.
        self.node_count += 1

        # Check if there are no moves available i.e. draw.
        if board.get_num_moves() == board.WIDTH * board.HEIGHT:
            print('draw')
            return 0

        # Check if the player can win the next move
        for y in range(board.HEIGHT):
            for x in range(board.WIDTH):
                if (board.is_valid_move((y, x))
                        and board.is_winning_move((y, x))):
                    print('p1 wins next move')
                    return (board.WIDTH * board.HEIGHT + 1
                            - board.get_num_moves()) // 2

        best_score = -(board.WIDTH * board.HEIGHT + 1 // 2)

        # Check all possible next moves and return the best one
        for y in range(board.HEIGHT):
            for x in range(board.WIDTH):
                if board.is_valid_move((y, x)):

                    print('Try this move:', (y, x))

                    check_next_move = copy.deepcopy(board)

                    check_next_move.show_board()
                    print('Move no. :', check_next_move.moves)

                    check_next_move.play((y, x))
                    score = -1 * self.negamax(check_next_move)

                    print(f'--- Board score for this branch {(y, x)}:', score,
                          '---')

                    if score > best_score:
                        best_score = score

                    print()

        return best_score

    def solve(self, board: board.Board) -> int:
        return self.negamax(board)

    def get_node_count(self) -> int:
        return self.node_count
