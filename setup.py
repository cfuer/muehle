import numpy as np

class Board:
    def __init__(self):
        self.layer = np.full((3, 8), np.nan)
        self.points = [0, 0]
        self.hand = [9, 9]
        self.player_pos = [[],[]]
        self.neighbour = self.neighbour_map()  #Attention: Type is a normal List not a Numpy List

    def __str__(self):
        a = np.full(24, '*')
        for i, d in enumerate(np.concatenate(self.layer)):
            if d == 1:
                a[i] = 'X'
            elif d == 0:
                a[i] = 'O'
        field = f'''{a[0]}------------{a[1]}------------{a[2]}
|            |            |
|   {a[8]}--------{a[9]}--------{a[10]}   |
|   |        |        |   |
|   |   {a[16]}----{a[17]}----{a[18]}   |   |
|   |   |         |   |   |
{a[3]}---{a[11]}---{a[19]}         {a[20]}---{a[12]}---{a[4]}
|   |   |         |   |   |
|   |   {a[21]}----{a[22]}----{a[23]}   |   |
|   |        |        |   |
|   {a[13]}--------{a[14]}--------{a[15]}   |
|            |            |
{a[5]}------------{a[6]}------------{a[7]}'''
        return field

    def info(self):
        field = f'''Um Steine zu setzten wähle die Positionen wie folgt aus.
        0,0----------------0,1----------------0,2
         |                  |                  |
         |    1,0----------1,1----------1,2    |
         |     |            |            |     |
         |     |    2,0----2,1----2,2    |     |
         |     |     |             |     |     |
        0,3---1,3---2,3           2,4---1,4---0,4
         |     |     |             |     |     |
         |     |    2,5----2,6----2,7    |     |
         |     |            |            |     |
         |    1,5----------1,6----------1,7    |
         |                  |                  |
        0,5----------------0,6----------------0,7
Möchtest du das Spiel zu einem Zeitpunkt beenden, dann returniere q. Dann wird das Spiel beendet.
Viel Spass beim Spielen!'''
        return field

    def neighbour_map(self):
        map = []
        addj = [[1,3], [0,2], [1,4], [0,5], [2,7], [3,6], [5,7], [4,6]]
        for i in range(3):
            tmp = []
            for j, m in enumerate(addj):
                tmp.append([])
                for t in m:
                    tmp[j].append((i,t))
                if j in [1,3,4,6]:
                    if i == 1:
                        tmp[j].extend([(0,j),(2,j)])
                    else:
                        tmp[j].append((1,j))
            map.append(tmp)
        return map

    def game_over(self, player):
        winner = (player+1) %2
        exit(f'Spieler {winner+1} hat das Spiel gewonnen!')

    def get_empty_positions(self):
        ep = []
        for a in range(3):
            for b in range(8):
                if np.isnan(self.layer[(a,b)]):
                    ep.append((a,b))
        return ep

    def is_valid(self, position):
        if 0<=position[0]<3 and 0<=position[1]<8:
            return np.isnan(self.layer[position])
        return False

    def is_valid_position_format(self, position, msg):
        positon = position.replace(' ', '')
        vp = {f'{i//8},{i%8}' for i in range(24)}
        if position in vp:
            return position.split(',')
        elif position == 'q':
            exit('Das Spiel wurde beendet')
        else:
            print("Bitte wähle eine valide Position")
            position = input(msg)
            return self.is_valid_position_format(position, msg)

    def moving_positions(self, player):
        if self.points[player] == 3:
            return self.player_pos[player]
        mp = []
        for pos in self.player_pos[player]:
            a, b = pos
            for neig in self.neighbour[a][b]:
                if self.is_valid(neig):
                    mp.append(pos)
                    break
        return mp

    def get_empty_neighbours(self, position):
        npo = []
        a, b = position
        for neig in self.neighbour[a][b]:
            if self.is_valid(neig):
                npo.append(neig)
        return npo

    def mill_check(self, position):
        l, p = position
        mill = False
        if p in [1,3,4,6]:
            mill = (self.layer[0, p] == self.layer[1, p] and self.layer[1, p] == self.layer[2, p])
        for r in [[0,1,2], [5,6,7], [2,4,7], [0,3,5]]:
            if mill:
                return True
            if p in r:
                mill = (self.layer[l, r[0]] == self.layer[l, r[1]] and self.layer[l, r[1]] == self.layer[l, r[2]])
        return mill

    def remove_opponent(self, player, position):
        if self.mill_check(position) or np.isnan(self.layer[position]) or self.layer[position] != player:
            print('Keine gültige Position. Bitte neu wählen.')
            pos = input('Welcher Stein soll entfernt werden? ')
            pos = self.is_valid_position_format(pos, 'Welcher Stein soll entfernt werden? ')
            return self.remove_opponent(player, (int(pos[0]), int(pos[1])))
        self.points[player] -= 1
        self.player_pos[player].remove(position)
        self.layer[position] = np.nan
        if self.points[player] < 3 and self.hand[player] == 0:
            return self.game_over(player)

    def place_coin(self, player, position):
        if self.is_valid(position):
            self.layer[position] = player
            self.points[player] += 1
            self.hand[player] -= 1
            self.player_pos[player].append(position)
            if self.mill_check(position):
                print(self.__str__())
                pos = input('Welcher Stein soll entfernt werden? ')
                pos = self.is_valid_position_format(pos, 'Welcher Stein soll entfernt werden? ')
                return self.remove_opponent((player+1)%2, (int(pos[0]), int(pos[1])))
        else:
            print('Keine gültige Position. Bitte neu wählen.')
            pos = input(f'Spieler {player+1} legt Stein: ')
            pos = self.is_valid_position_format(pos, f'Spieler {player+1} legt Stein: ')
            return self.place_coin(player, (int(pos[0]), int(pos[1])))

    def move_coin(self, player, position, move):
        self.layer[position] = np.nan
        self.player_pos[player].remove(position)
        self.layer[move] = player
        self.player_pos[player].append(move)
        if self.mill_check(move):
            print(self.__str__())
            pos = input('Welcher Stein soll entfernt werden? ')
            pos = self.is_valid_position_format(pos, 'Welcher Stein soll entfernt werden? ')
            return self.remove_opponent((player+1)%2, (int(pos[0]), int(pos[1])))
