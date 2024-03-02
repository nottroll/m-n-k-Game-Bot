import board

MAX_DISPLAY_WIDTH = 60
LPAD = 3

def print_state_score(board_state: board.Board, move_scores: list):
    print('Board')
    if board_state.board is None:
        print('Empty Board')

    for y in range(board.N):
        for x in range(board.M):
            if board_state.board[y][x] == 1:
                print(f'{board.TOKENS[0]:>{LPAD}}', end='')
            elif board_state.board[y][x] == 2:
                print(f'{board.TOKENS[1]:>{LPAD}}', end='')
            else:
                print(f'{".":>{LPAD}}', end='')
        print()
    print()

    print('Move scores')
    for y in range(board.N):
        for x in range(board.M):
            if move_scores[y][x] is None:
                print(f'{".":>{LPAD}}', end='')
            else:
                print(f'{move_scores[y][x]:>{LPAD}}', end='')
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
    
def print_divider():
    print('-' * MAX_DISPLAY_WIDTH)

def print_solve_stats(search_nodes, solve_time):
    print(f'Searched nodes: {search_nodes}', 
          f'Solve time:     {(solve_time) * 1000:.2f}ms', 
          sep='\n', end='\n\n')

def win_message(player: int):
    print(f'Player {player} wins!')

def draw_message():
    print('Draw!')