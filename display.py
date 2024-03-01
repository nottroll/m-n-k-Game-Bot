import board

def print_state_score(board_state: board.Board, move_scores: list):
    print('Board')
    if board_state.board is None:
        print('Empty Board')

    for y in range(board.N):
        for x in range(board.M):
            if board_state.board[y][x] == 1:
                print(' X', end='')
            elif board_state.board[y][x] == 2:
                print(' O', end='')
            else:
                print(' .', end='')
        print()
    print()

    print('Move scores')
    for y in range(board.N):
        for x in range(board.M):
            if move_scores[y][x]:
                print(f'{move_scores[y][x]:>2}', end='')
            else:
                print(' .', end='')
        print()
    print()


def print_score_explanation():
    print('--- Scoring explanation ---',
          ' 0 = P1 or P2 can draw (neutral move)',
          '>0 = P1 can force a win (more positive is better for P1)',
          '<0 = P2 can force a win (more negative is better for P2)',
          '',
          '--- Strategy ---',
          'P1 should choose the most positive number or 0',
          'P2 should choose the most negative number or 0', 
          sep='\n', end='\n\n')