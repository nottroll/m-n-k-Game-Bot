import board
import solver

if __name__ == '__main__':
    curr_move = 0
    solve = solver.Solver()
    board_state = board.Board()

    for _ in range(10):
        print(f'\nMove {curr_move}')
        print('Board')
        board_state.show_board()

        print('Move scores')
        score = solve.solve_score_each(board_state)
        min_score, max_score = min(score), max(score)

        print('Best move p1 score:', max_score)
        print('Best move p2 score:', min_score)
        print('Searched Nodes:', solve.get_node_count())

        inp = input('Which move to play? Enter in format row,col e.g. 1,1: \n >>> ')
        move = tuple([int(i) for i in inp.split(',')])

        board_state.play(move)

