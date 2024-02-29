import board
import solver

if __name__ == '__main__':
    curr_move = 0
    s = solver.Solver()

    for _ in range(1):
        b = board.Board()
        b.show_board()


        inp = input('Play move r,c:')
        move = tuple([int(i) for i in inp.split(',')])

        b.play(move)

        score = s.solve(b)
        b.show_board()

        print('Best move eval score:', score)
        print('Searched Nodes:', s.get_node_count())
