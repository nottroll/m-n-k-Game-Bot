"""
Alson Lee
Date: 02/03/24

The display module handles simple console output.
"""

import board

MAX_DISPLAY_WIDTH = 60
LPAD = 4


def print_state_score(board_state: board.Board, move_scores: list):
    """
    Prints a board state and its scores.
    :param board_state: the board state
    :param move_scores: the scores for the board state
    """
    curr_player = f'{board_state.position:0{board.M*board.N}b}'
    next_player = f'{board_state.position^board_state.mask:0{board.M*board.N}b}'

    if board_state.get_num_moves() % 2 == 0:
        P1, P2 = curr_player, next_player # P1 on even turns
    else:
        P1, P2 = next_player, curr_player

    print('Board')
    for r in range(board.N):
        for c in range(board.M):
            if P1[-(r * board.M + c + 1)] == '1':
                print(f'{board.TOKENS[0]:>{LPAD}}', end='')
            elif P2[-(r * board.M + c + 1)] == '1':
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

def print_board_cells():
    """
    Prints the board cell numbers.
    """
    print('Board cells')
    for r in range(board.N):
        for c in range(board.M):
            print(f'{r*board.M + c + 1:>{LPAD}}', end='')
        print()
    print()


def print_score_explanation():
    """
    Prints an explanation for the scoring.
    """
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
