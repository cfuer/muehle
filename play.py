from setup import Board

board = Board()
player = 0

print(board.info())

for i in range(18):
    pos = input(f'Spieler {player+1} legt Stein: ')
    pos = board.is_valid_position_format(pos, f'Spieler {player+1} legt Stein: ')
    board.place_coin(player, (int(pos[0]), int(pos[1])))
    player = (player+1) % 2
    print(board)

while True:
    if board.points != 3:
        mov_pos = board.moving_positions(player)
    else:
        mov_pos = board.player_pos[player]
    idx = 0
    if len(mov_pos) == 0:
        board.game_over(player)
    while idx <= 0 or idx > len(mov_pos):
        for i, mp in enumerate(mov_pos, start=1):
            print(f'({i}) Stein {mp}')
        idx = input(f'Spieler {player+1}: Welcher Stein soll verschoben werden [1-{len(mov_pos)}]? ')
        try:
            idx = int(idx)
        except:
            if idx == 'q':
                exit('Das Spiel wurde beendet')
            print("Kein valider Stein. Bitte wähle erneut:")
    pos = mov_pos[idx-1]
    if board.points[player] != 3:
        neig_pos = board.get_empty_neighbours(pos)
    else:
        neig_pos = board.get_empty_positions()
    idx = 0
    if len(neig_pos) != 1:
        while idx <= 0 or idx > len(neig_pos):
            for i, npo in enumerate(neig_pos, start=1):
                print(f'({i}) Position {npo}')
            idx = input('Wohin? ')
            try:
                idx = int(idx)
            except:
                if idx == 'q':
                    exit('Das Spiel wurde beendet')
                print("Keine valide Position. Bitte wähle erneut:")
    else:
        idx = 1
    new_pos = neig_pos[idx-1]
    board.move_coin(player, pos, new_pos)
    player = (player+1) % 2
    print(board)
