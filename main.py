import board
import display
import solver
import timeit

if __name__ == '__main__':
    # TODO: allow user to configure board m,n,k
    
    solve = solver.Solver()
    board_state = board.Board()
    curr_move = 0

    # Game and solver loop
    while curr_move <= board.N * board.M:
        display.print_divider()
        
        curr_player = 1 + curr_move % 2
        print(f'Moves played: {curr_move}', 
              f'Turn: Player {curr_player}',
              f'Player token: {board.TOKENS[0] if curr_player == 1 else board.TOKENS[1]}',
              sep='  |  ', end='\n\n')
        
        # Solve and time performance
        solve_start = timeit.default_timer()
        move_scores = solve.solve_score_each(board_state)
        solve_end = timeit.default_timer()

        display.print_state_score(board_state, move_scores)

        solve_stats = solve.get_node_count()
        display.print_solve_stats(solve_stats, solve_end - solve_start)
        solve.reset_node_count()

        display.print_score_explanation()
        
        inp = input('Which move to play? Enter in format row,col e.g. 1,1: \n >>> ')
        move = tuple([int(i) for i in inp.split(',')])

        if board_state.is_winning_move(move):
            board_state.play(move)
            display.win_message(curr_player)
            display.print_state_score(board_state, move_scores)
            break

        board_state.play(move)
        curr_move += 1

    else:
        display.draw_message()
