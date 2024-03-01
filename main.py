import board
import display
import solver
import timeit


if __name__ == '__main__':
    curr_move = 0
    solve = solver.Solver()
    board_state = board.Board()

    while curr_move <= board.N * board.M:
    # for _ in range(10):
        print('-'*50)

        print(f'\nMoves played: {curr_move}', 
              f'Turn: Player {1 + curr_move % 2}',
              f'Player token: {"X" if 1 + curr_move % 2 == 1 else "O"}',
              sep='  |  ', end='\n\n')
        
        # Solve and time performance
        solve_start_time = timeit.default_timer()
        move_scores = solve.solve_score_each(board_state)
        solve_end_time = timeit.default_timer()

        display.print_state_score(board_state, move_scores)

        solve_stats = solve.get_node_count()
        print(f'Searched nodes: {solve_stats}', 
              f'Solve time: {(solve_end_time-solve_start_time)*1000:.2f}ms', 
              sep='\n', end='\n\n')
        solve.reset_node_count()

        display.print_score_explanation()
        
        inp = input('Which move to play? Enter in format row,col e.g. 1,1: \n >>> ')
        move = tuple([int(i) for i in inp.split(',')])

        if board_state.is_winning_move(move):
            board_state.play(move)
            print(f'Player {1 + curr_move % 2} wins!')
            display.print_state_score(board_state, move_scores)
            break

        board_state.play(move)
        curr_move += 1

    else:
        print('Draw!')
