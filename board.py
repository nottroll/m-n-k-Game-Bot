"""
Alson Lee
Date: 06/03/24 

The board module contains the board game logic for an m,n,k-game.
"""

TOKENS = ('X', 'O')  # The symbols for the players
M = 4                # Board of m width
N = 4                # Board of n height
K_IN_ROW = 3         # Require k tokens in a line to win

# TODO: Optimise solver to handle larger cases.
assert M <= 6 and N <= 6, 'M and N must too large'
assert K_IN_ROW <= M and K_IN_ROW <= N, 'K_IN_ROW too large'

"""
Class to represent a board state for an m,n,k-game
"""
class Board:
    """
    Each board cell is represented with a position bit and mask bit.
    Position and mask is M*N bits. The key = Position + Mask is M*N+1 bits
    
    Bit order      Board       Position    Mask        Key = Position + Mask
     0  1  2  3    0 X 0 O     0 1 0 0     0 1 0 1     
     4  5  6  7    0 0 X 0     0 0 1 0     0 0 1 0 
     8  9 10 11    0 O 0 0     0 0 0 0     0 1 0 0 
    12 13 14 15    0 0 0 0     0 0 0 0     0 0 0 0 

    """
    MIN_SCORE = -(M * N) // 2 - 1
    MAX_SCORE = M * N // 2 + 1

    def __init__(self, position=0, mask=0, moves=0):
        self.position = position
        self.mask = mask
        self.moves = moves  # number of moves played

    def is_valid_move(self, move: int) -> bool:
        """
        Checks if the move is valid.
        :param move: the move to play
        :return:     if the move is valid
        """
        if 0 <= move < M * N and self.mask & (1 << move) == 0:
            return True
        return False

    def play(self, move: int):
        """
        Plays a move.
        :param move: the move to play
        """
        self.position ^= self.mask
        self.mask |= 1 << move
        self.moves += 1

    def play_sequence(self, moves: list) -> int:
        """
        Plays a sequence of moves.
        :param moves: a list of moves to play
        :return:      the number of moves to be played.
        """
        for move in moves:
            if self.is_winning_move(move):
                break
            self.play(move)
        return len(moves)
    
    def is_winning_move(self, move: int) -> bool:
        """
        Checks whether the move is a winning move.
        :param move: the move to check
        :return:     if the move is a winning move
        """
        # Check next_pos if move is played. 
        next_pos = self.position
        next_pos |= 1 << move
        # print(f'next: {next_pos:0{M*N}b}')

        # Check the row of the token played for winning.
        # A winning row will have k-in-a-row bits set.
        # E.g. 4,3,3-game: 0000 1110 0000 wins
        # check_r is the checking mask for k-in-a-row bits set:
        check_r = (1 << K_IN_ROW) - 1
        for shift in range(0, M - K_IN_ROW + 1):
            # shift will check all positions within a row: 
            # E.g. 5,5,3-game: 11100 -> 01110 -> 00111
            shift_r = next_pos >> (move // M * M) + shift
            if check_r & shift_r == check_r:
                return True
        
        # Check the col of the token played for winning.
        # check_c is the checking mask for bits set at indices move % M:
        # E.g. 4,3,3-game: 0100 0100 0100 wins
        check_c = 1 << (move % M) 
        for _ in range(K_IN_ROW-1):
            check_c <<= M
            check_c |= 1 << (move % M) 

        for shift in range(0, N - K_IN_ROW + 1):
            shift_c = next_pos >> (shift * M)
            # shift next_pos by M bits until there is a match with check_c: 
            if check_c & shift_c == check_c:
                return True


        # TODO: Implement bitwise checking for diagonals.
            
        # Check diagonal NW-SE direction
        d1 = [(move // M + i) * M + move % M + i 
              if (0 <= (move // M + i) < N and 0 <= (move % M + i) < M) 
              else -1 
              for i in range(-K_IN_ROW + 1, K_IN_ROW)]
        # print('d1', d1)
        for i in range(len(d1) - K_IN_ROW + 1):
            check_d1 = 0
            if d1[i] != -1 and d1[i+K_IN_ROW-1] != -1:
                for j in range(K_IN_ROW):
                    check_d1 |= 1 << d1[i+j]
                if check_d1 & next_pos == check_d1:
                    return True
        

        # Check diagonal NE-SW direction
        d2 = [(move // M + i) * M + move % M - i 
              if (0 <= (move // M + i) < N and 0 <= (move % M - i) < M) 
              else -1 
              for i in range(-K_IN_ROW + 1, K_IN_ROW)]
        # print(d2)
        for i in range(len(d2) - K_IN_ROW + 1):
            check_d2 = 0
            if d2[i] != -1 and d2[i+K_IN_ROW-1] != -1:
                for j in range(K_IN_ROW):
                    # print(i, j)
                    check_d2 |= 1 << d2[i+j]
                if check_d2 & next_pos == check_d2:
                    return True

        return False

    def get_num_moves(self) -> int:
        """
        Returns the number of moves played.
        :return: the number of moves played
        """
        return self.moves

       

# b = Board([[2, 1, 0],
#            [0, 1, 0],
#            [2, 0, 0]], 4)

# print(b.is_winning_move((0,0)))
# print(b.is_winning_move((1,0)))
# print(b.is_winning_move((2,1)))

# for r in range(N):
#     for c in range(M):
#         print(f'{r*M + c:>4}', end='')
#     print()
# print()

# b = Board()

# b.play_sequence([5])

# print(f'pos: {b.position:0{M*N}b}', f'mask: {b.mask:0{M*N}b}')
# print(b.is_winning_move(2))
