"""
Alson Lee
Date: 02/03/24

The display module handles simple console output.
"""

import board

MAX_DISPLAY_WIDTH = 60
LPAD = 4

def print_board_cells(board_state: board.Board):
    """
    Prints the board cell numbers.
    """
    print('Board cells')
    for r in range(board_state.N):
        for c in range(board_state.M):
            print(f'{r*board_state.M + c + 1:>{LPAD}}', end='')
        print()
    print()


def print_board_state(board_state: board.Board):
    """
    Prints a board state.
    :param board_state: the board state
    """
    curr_player = f'{board_state.position:0{board_state.M*board_state.N}b}'
    next_player = f'{board_state.position^board_state.mask:0{board_state.M*board_state.N}b}'

    if board_state.get_num_moves() % 2 == 0:
        P1, P2 = curr_player, next_player # P1 on even turns
    else:
        P1, P2 = next_player, curr_player

    print('Board')
    for r in range(board_state.N):
        for c in range(board_state.M):
            if P1[-(r * board_state.M + c + 1)] == '1':
                print(f'{board_state.tokens[0]:>{LPAD}}', end='')
            elif P2[-(r * board_state.M + c + 1)] == '1':
                print(f'{board_state.tokens[1]:>{LPAD}}', end='')
            else:
                print(f'{".":>{LPAD}}', end='')
        print()
    print()


def print_board_score(board_state: board.Board, move_scores: list):
    """
    Prints the scores of a board.
    :param board_state: the board state
    :param move_scores: the scores for the board state
    """
    player = 1 if board_state.get_num_moves() % 2 else 2        
    scores = set()
    for y in range(board_state.N):
        for x in range(board_state.M):
            if move_scores[y][x] is not None:
                scores.add(move_scores[y][x])
    
    best_move = max(scores)

    print(f'Move scores for Player {player}')
    for y in range(board_state.N):
        for x in range(board_state.M):
            score = move_scores[y][x]
            if score is None:
                print(f'{".":>{LPAD}}', end='')
            else:
                fscore = score if score != best_move else '*' + str(score)
                print(f'{fscore:>{LPAD}}', end='')
        print()
    print()


def print_score_explanation(board_state: board.Board):
    """
    Prints an explanation for the scoring.
    """
    if board_state.get_num_moves() % 2 == 0:
        curr_player, next_player = 1, 2 # P1 on even turns
    else:
        curr_player, next_player = 2, 1
    print('--- Scoring explanation ---',
          ' 0 = A move which could force a draw',
          f'>0 = Current player (P{curr_player}) can force a win (more positive is better for P{curr_player})',
          f'<0 = Opponent (P{next_player}) can force a win (more negative is better for P{next_player})',
          '',
          '--- Strategy ---',
          'The current player should choose the most positive number',
          ' * marks the best moves for the current player',
          sep='\n', end='\n\n')


def print_divider():
    """
    Prints a divider.
    """
    print('-' * MAX_DISPLAY_WIDTH)


def print_solve_stats(search_nodes: int, solve_time: float):
    """
    Prints the solving stats.
    :param search_nodes: number of nodes explored
    :param solve_time:   the time to solve
    """
    print(f'Searched nodes: {search_nodes}',
          f'Solve time:     {solve_time * 1000:.2f}ms',
          sep='\n', end='\n\n')


def win_message(player: int):
    """
    Prints a message for the winning player.
    :param player: the winning player
    """
    print(f'Player {player} wins!')


def draw_message():
    """
    Prints a message if the game is drawn.
    """
    print('Draw!')
