a = 60
b = -30
c = -40
d = 25
e = -25
f = 1
v = 5

A = [(i,j) for i in [0,7] for j in [0,7]]
C = [(i,j) for i in [1,6] for j in [1,6]]
B = [(i,j) for i in [0,1,6,7] for j in [0,1,6,7] if i != j and (i,j) not in A and (i,j) not in C]
D = [(0,j) for j in [2,3,4,5]] + [(7,j) for j in [2,3,4,5]] \
  + [(i,0) for i in [2,3,4,5]] + [(i,7) for i in [2,3,4,5]]
E = [(1,j) for j in [2,3,4,5]] + [(6,j) for j in [2,3,4,5]] \
  + [(i,1) for i in [2,3,4,5]] + [(i,6) for i in [2,3,4,5]]
F = [(i,j) for i in [2,3,4,5] for j in [2,3,4,5]]

wart = [a,b,c,d,e,f]
typy = [A,B,C,D,E,F]

tablica_wag = {}
for k in range(len(typy)):
    for t in typy[k]:
        tablica_wag[t] = wart[k]

kierunki = [ (0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]

def can_beat(board, x,y, d, player):
    dx,dy = d
    x += dx
    y += dy
    cnt = 0
    while get(board,x,y) == -player:
        x += dx
        y += dy
        cnt += 1
    return cnt > 0 and get(board,x,y) == player

def get(board, x,y):
    if 0 <= x < 8 and 0 <= y < 8:
        return board[y][x]
    return None

def ruchy(wezel, gracz):
    res = []
    for (x,y) in wezel.fields:
        if any(can_beat(wezel.board,x,y, direction, gracz) for direction in kierunki):
            res.append( (x,y) )
    if not res:
        return [wezel]
    return [Node(wezel.board,r,gracz) for r in res]

class Node:
    def __init__(self,plansza,ruch,gracz):
        self.board = plansza
        self.gracz = gracz
        self.board[ruch[0]][ruch[1]] = gracz
        self.fields = set()
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    self.fields.add( (j,i) )

def heurystyka(wezel,v=v):
    return sum([wezel.board[i][j]*tablica_wag[(i,j)] for i in range(8) for j in range(8)]) + v*len(ruchy(wezel,wezel.gracz))

def minMaxAlfaBeta(wezel, d, alfa, beta):
    if  d == 0 or ruchy(wezel,-1) == [None] or ruchy(wezel,1) == [None] or len(wezel.fields) == 0:
        return heurystyka(wezel)
    if wezel.gracz == -1:
        for w in ruchy(wezel,1):
            beta = min(beta, minMaxAlfaBeta(w, d-1, alfa, beta))
            if alfa >= beta:
                break
        return beta
    else:
        for w in ruchy(wezel,-1):
            if w == None:
                break
            alfa = max(alfa, minMaxAlfaBeta(w, d-1, alfa, beta))
            if alfa >= beta:
                break
        return alfa
