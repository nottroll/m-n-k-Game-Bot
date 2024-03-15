# Solver for m,n,k-game

This project implements an AI which uses the negamax algorithm to solve the m,n,k-game.

The m,n,k-game is a 2-player game played on a m-by-n board where the goal is to have k-in-a-line either horizontally, vertically or diagonally. Each player takes turns to put down their token on a free board space until a player wins or draw if all free spaces have been used.

With parameters m=3,n=3,k=3, the game is an instance of tic-tac-toe.

See more information here: (https://en.wikipedia.org/wiki/M,n,k-game)

## Negamax Algorithm
The negamax algorithm is a simplification of the minimax algorithm using the fact that m,n,k-games are zero-sum i.e. the gain of one player is equal to the loss of the other. Specifically, `min(state) = -max(-state)`. The algorithm performs a depth-first search down the game tree for any given move until a winning move is found. A strong solver is implemented which searches through the entire tree. The score of that move depends on how quickly the current player can win. Assign positive values to player 1, and negative values to player 2. A move with the higher positive value is the better move for player 1 and a move with the higher negative value is better for player 2. A score of 0 is a neutral move which can result in a draw.

## Alpha-beta pruning
Alpha-beta pruning is an optimisation which prevents the search algorithm from searching a move which is definitely worse than a previously searched move. `alpha` represents the min score for the maximising player (P1) and `beta` represents the max score for the minimising player (P2). As the algorithm searches, it keeps track of a score window `[alpha, beta]`. For exmaple, the algorithm finds a score of 10 for P1, hence for any further searches there is no need to explore scores >10 as the goal is to maximise the score of P1. 

## Bitboard
Each board state is represented with 2 m*n bit integers: position and a mask. The position encodes the current players pieces and the mask encode all pieces played so far. The each turn the subsequent players pieces can be easily recovered with `position XOR mask`.
```    
Bit order      Board          Position       Mask        
 0  1  2  3    .  X  .  O     0  1  0  0     0  1  0  1     
 4  5  6  7    .  .  X  .     0  0  1  0     0  0  1  0 
 8  9 10 11    .  O  .  .     0  0  0  0     0  1  0  0 
12 13 14 15    .  .  .  .     0  0  0  0     0  0  0  0 
```

## Search Order
Moves are searched in an outwards spiral which unwinds from the middle in the clockwise direction. The idea is that moves played near the centre have more impactful branches which will create more opportunities for alpha-beta pruning.
```    
Search order   
16 15 14 13    
 5  4  3 12
 6  1  2 11
 7  8  9 10
```
