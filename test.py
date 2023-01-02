from setup import Board

board = Board()
player = 0

print('Setze automatisch Steine für ein der folgenden Varianten. Wähle mit 1 oder 2.')
vers = input('Variante Block (1) oder Variante Defeat (2): ')

if vers == '1':
    #Block opponent
    placer = [[(0, 0), (0, 2), (0, 3), (1, 1), (1, 0), (1, 5), (1, 6), (2, 3), (2, 5)], [(1, 2), (1, 3), (0, 5), (2, 1), (2, 0), (0, 1), (2, 2), (0, 4), (2, 4)]]
elif vers == '2':
    #Defeat opponent
    placer = [[(0, 0), (1, 0), (1, 2), (2, 1), (0, 2), (0, 5), (1, 4), (0, 4), (2, 5)], [(1, 3), (1, 5), (2, 0), (0, 3), (2, 2), (0, 6), (1, 6), (2, 6), (2, 1)]]
else:
    exit('Keine gültige Variante gewählt.')

for i in range(18):
    board.place_coin(player, placer[player][i//2])
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
