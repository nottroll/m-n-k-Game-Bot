"""
Class to represent a board state
"""


class Board:
    WIDTH = 3
    HEIGHT = 3
    win_cond = 3  # no. of tokens in a line to win
    assert win_cond <= WIDTH and win_cond <= HEIGHT, 'win_cond too large'
    MIN_SCORE = WIDTH * HEIGHT // 2 + 1
    MAX_SCORE = -(WIDTH * HEIGHT) // 2 - 1

    # 0 is empty, 1 is player1, 2 is player2
    def __init__(self,
                 board=None,
                 moves=0):
        if board is None:
            board = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
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
        if (not (0 <= play_x < self.WIDTH) or
                not (0 <= play_y < self.HEIGHT) or
                not self.is_valid_move(move)):
            return False

        # Create range to check
        range_x = [x for x in
                   range(play_x - self.win_cond + 1, play_x + self.win_cond)]
        range_y = [y for y in
                   range(play_y - self.win_cond + 1, play_y + self.win_cond)]

        # Check rows "-" for winning by counting tokens for the current player.
        count_x = 1
        for dx in range_x:
            if (0 <= dx < self.WIDTH
                    and self.board[play_y][dx] == curr_player):
                count_x += 1
        if count_x == self.win_cond:
            return True

        # Check cols "|" for winning by counting tokens for the current player.
        count_y = 1
        for dy in range_y:
            if (0 <= dy < self.HEIGHT
                    and self.board[dy][play_x] == curr_player):
                count_y += 1
        if count_y == self.win_cond:
            return True

        # Check diagonals NW-SE "\" for winning
        count_d1 = 1
        for dx, dy in zip(range_x, range_y):
            if (0 <= dx < self.WIDTH and 0 <= dy < self.HEIGHT
                    and self.board[dy][dx] == curr_player):
                count_d1 += 1
        if count_d1 == self.win_cond:
            return True

        # Check diagonals NE-SW "/" for winning
        count_d2 = 1
        for dx, dy in zip(range_x, reversed(range_y)):
            if (0 <= dx < self.WIDTH and 0 <= dy < self.HEIGHT
                    and self.board[dy][dx] == curr_player):
                count_d2 += 1
        if count_d2 == self.win_cond:
            return True

        return False

    def get_num_moves(self) -> int:
        """
        Returns the number of moves played
        :return:
        """
        return self.moves

    def show_board(self):
        if self.board is None:
            print('Empty')

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.board[y][x] == 1:
                    print('X', end='')
                elif self.board[y][x] == 2:
                    print('O', end='')
                else:
                    print('.', end='')
            print()
        print()

# b = Board([[0, 1, 2],
#            [0, 2, 1],
#            [0, 1, 0]], 5)

# print(b.isWinningMove((0,0)))
# print(b.isWinningMove((1,0)))
# print(b.isWinningMove((1,1)))
# print(b.isWinningMove((2,0)))
