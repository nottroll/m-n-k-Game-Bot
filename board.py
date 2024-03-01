"""

"""

M = 3  # Board of m width
N = 3  # Board of n height
K_IN_ROW = 3  # Require k tokens in a line to win
assert M < 10 and N < 10, 'M and N must be less than 10'
assert K_IN_ROW <= M and K_IN_ROW <= N, 'K_IN_ROW too large'

"""
Class to represent a board state
"""
class Board:
    MIN_SCORE = -(M * N) // 2 - 1
    MAX_SCORE = M * N // 2 + 1

    # 0 is empty, 1 is player1, 2 is player2
    def __init__(self,
                 board=None,
                 moves=0):
        if board is None:
            board = [[0 for _ in range(M)] for _ in range(N)]
        self.board = board
        self.moves = moves

    def is_valid_move(self, move: tuple) -> bool:
        """
        Checks if the move is valid
        :param move:
        :return:
        """
        y, x = move
        return True if self.board[y][x] == 0 else False

    def play(self, move: tuple):
        """
        Plays a move
        :param move:
        :return:
        """
        if self.is_valid_move(move):
            y, x = move
            self.board[y][x] = 1 + self.moves % 2
            self.moves += 1

    def play_sequence(self, moves: list[tuple]) -> int:
        """
        Plays a sequence of moves
        :param moves:
        :return:
        """
        for move in moves:
            if self.is_winning_move(move):
                break
            self.play(move)
        return len(moves)

    def is_winning_move(self, move: tuple) -> bool:
        """
        Checks whether the move (row, col) or (y, x) is a winning move.
        :param move:
        :return:
        """
        play_y, play_x = move
        curr_player = 1 + self.moves % 2

        # Check valid move
        if (not (0 <= play_x < M) or
                not (0 <= play_y < N) or
                not self.is_valid_move(move)):
            return False

        # Create range to check
        range_x = [x for x in
                   range(play_x - K_IN_ROW + 1, play_x + K_IN_ROW)]
        range_y = [y for y in
                   range(play_y - K_IN_ROW + 1, play_y + K_IN_ROW)]

        # Check rows "-" for winning by counting tokens for the current player.
        count_x = 1
        for dx in range_x:
            if (0 <= dx < M
                    and self.board[play_y][dx] == curr_player):
                count_x += 1
        if count_x == K_IN_ROW:
            return True

        # Check cols "|" for winning by counting tokens for the current player.
        count_y = 1
        for dy in range_y:
            if (0 <= dy < N
                    and self.board[dy][play_x] == curr_player):
                count_y += 1
        if count_y == K_IN_ROW:
            return True

        # Check diagonals NW-SE "\" for winning
        count_d1 = 1
        for dx, dy in zip(range_x, range_y):
            if (0 <= dx < M and 0 <= dy < N
                    and self.board[dy][dx] == curr_player):
                count_d1 += 1
        if count_d1 == K_IN_ROW:
            return True

        # Check diagonals NE-SW "/" for winning
        count_d2 = 1
        for dx, dy in zip(range_x, reversed(range_y)):
            if (0 <= dx < M and 0 <= dy < N
                    and self.board[dy][dx] == curr_player):
                count_d2 += 1
        if count_d2 == K_IN_ROW:
            return True

        return False

    def get_num_moves(self) -> int:
        """
        Returns the number of moves played
        :return:
        """
        return self.moves

# b = Board([[2, 1, 0],
#            [0, 1, 0],
#            [2, 0, 0]], 4)

# print(b.is_winning_move((0,0)))
# print(b.is_winning_move((1,0)))
# print(b.is_winning_move((2,1)))
# print(b.is_winning_move((1,2)))
# print(b.is_winning_move((2,0)))
