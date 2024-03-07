"""
Alson Lee
Date: 06/03/24 

The board module contains the board game logic for an m,n,k-game.
"""


"""
Class to represent a board state for an m,n,k-game
"""
class Board:
    """
    Each board cell is represented with a position bit and mask bit.
    Integers position and mask are M*N bits. The key = position + mask is M*N+1 bits.
    
    Bit order      Board          Position       Mask        
     0  1  2  3    .  X  .  O     0  1  0  0     0  1  0  1     
     4  5  6  7    .  .  X  .     0  0  1  0     0  0  1  0 
     8  9 10 11    .  O  .  .     0  0  0  0     0  1  0  0 
    12 13 14 15    .  .  .  .     0  0  0  0     0  0  0  0 

    """

    def __init__(self, tokens = ('X', 'O'), 
                 M = 3, N = 3, k_in_row = 3, 
                 position=0, mask=0, moves=0):
        self.tokens = tokens         # The symbols for the players
        self.M = M                   # Board of m width
        self.N = N                   # Board of n height
        self.k_in_row = k_in_row     # Require k tokens in a line to win

        # TODO: Optimise solver to handle larger cases.
        assert self.M <= 6 and self.N <= 6, 'M and N too large'
        assert self.k_in_row <= self.M and self.k_in_row <= self.N, 'k_in_row too large'

        self.position = position  # encoding of pieces for the current player
        self.mask = mask          # encoding of all pieces played
        self.moves = moves        # number of moves played
        
        self.min_score = -(self.M * self.N) // 2 + 3
        self.max_score = (self.M * self.N + 1) // 2 - 3

    def is_valid_move(self, move: int) -> bool:
        """
        Checks if the move is valid.
        :param move: the move to play
        :return:     if the move is valid
        """
        if 0 <= move < self.M * self.N and self.mask & (1 << move) == 0:
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
        # print(f'next: {next_pos:0{self.M*N}b}')

        # Check the row of the token played for winning.
        # A winning row will have k-in-a-row bits set.
        # E.g. 4,3,3-game: 0000 1110 0000 wins
        # check_r is the checking mask for k-in-a-row bits set:
        check_r = (1 << self.k_in_row) - 1
        for shift in range(0, self.M - self.k_in_row + 1):
            # shift will check all positions within a row: 
            # E.g. 5,5,3-game: 11100 -> 01110 -> 00111
            shift_r = next_pos >> (move // self.M * self.M) + shift
            if check_r & shift_r == check_r:
                return True
        
        # Check the col of the token played for winning.
        # check_c is the checking mask for bits set at indices move % M:
        # E.g. 4,3,3-game: 0100 0100 0100 wins
        check_c = 1 << (move % self.M) 
        for _ in range(self.k_in_row-1):
            check_c <<= self.M
            check_c |= 1 << (move % self.M) 

        for shift in range(0, self.N - self.k_in_row + 1):
            shift_c = next_pos >> (shift * self.M)
            # shift next_pos by M bits until there is a match with check_c: 
            if check_c & shift_c == check_c:
                return True


        # TODO: Implement bitwise checking for diagonals.
            
        # Check diagonal NW-SE direction
        d1 = [(move // self.M + i) * self.M + move % self.M + i 
              if (0 <= (move // self.M + i) < self.N and 0 <= (move % self.M + i) < self.M) 
              else -1 
              for i in range(-self.k_in_row + 1, self.k_in_row)]

        for i in range(len(d1) - self.k_in_row + 1):
            check_d1 = 0
            if d1[i] != -1 and d1[i+self.k_in_row-1] != -1:
                for j in range(self.k_in_row):
                    check_d1 |= 1 << d1[i+j]
                if check_d1 & next_pos == check_d1:
                    return True

        # Check diagonal NE-SW direction
        d2 = [(move // self.M + i) * self.M + move % self.M - i 
              if (0 <= (move // self.M + i) < self.N and 0 <= (move % self.M - i) < self.M) 
              else -1 
              for i in range(-self.k_in_row + 1, self.k_in_row)]

        for i in range(len(d2) - self.k_in_row + 1):
            check_d2 = 0
            if d2[i] != -1 and d2[i+self.k_in_row-1] != -1:
                for j in range(self.k_in_row):
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
    
    def key(self) -> int:
        return self.position + self.mask

       

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
