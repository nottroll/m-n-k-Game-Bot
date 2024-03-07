"""
Alson Lee
Date: 06/03/24

Simple AI using negamax algorithm to solve m,n,k-games
"""

import board
import display
import solver
import validation

import timeit

"""
GAME SETTINGS
"""
BOARD_WIDTH = 3   # Set the board width
BOARD_HEIGHT = 3  # Set the board height
K_IN_A_ROW = 3    # Set number of tokens in a row to win

def main():
    # TODO: allow user to configure board m,n,k

    board_state = board.Board(N=BOARD_WIDTH, M=BOARD_HEIGHT, k_in_row=K_IN_A_ROW)
    solve = solver.Solver(board_state)
    curr_move = 0

    # Game and solver loop
    board_cells = board_state.M * board_state.N
    while curr_move < board_cells:
        display.print_divider()
        
        curr_player = 1 + curr_move % 2  # Move 0 is P1, Move 1 is P2 etc.
        print(f'Player {curr_player}',
              f'Moves played: {curr_move}', 
              f'Player token: {board_state.tokens[0] if curr_player == 1 else board_state.tokens[1]}',
              sep='  |  ', end='\n\n')
        
        # Solver performance
        solve_start = timeit.default_timer()
        move_scores = solve.solve_score_each(board_state)
        solve_end = timeit.default_timer()
        
        solve_stats = solve.get_node_count()

        # Display board and solve scores to console
        display.print_board_cells(board_state)
        display.print_board_state(board_state)
        display.print_board_score(board_state, move_scores)
        display.print_solve_stats(solve_stats, solve_end - solve_start)
        solve.reset_node_count()

        display.print_score_explanation(board_state)
        
        move = 1
        while True:
            print(f'Which board cell to play? Enter a cell between (0-{board_cells}):')
            inp = input(' >>> ')
            if validation.is_valid_input(inp) and 0 < move <= board_cells:
                move = int(inp) - 1
                break

        # Check win
        if board_state.is_winning_move(move):
            board_state.play(move)
            display.print_board_state(board_state)
            display.win_message(curr_player)
            break

        board_state.play(move)
        curr_move += 1

    else:
        display.print_board_state(board_state)
        display.draw_message()

if __name__ == '__main__':
    main()
