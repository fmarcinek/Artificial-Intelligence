import random
import sys
from collections import defaultdict as dd
from turtle import *
from reversi import *

#####################################################
# turtle graphic
#####################################################
# tracer(0,1)

BOK = 30
SX = -100
SY = 0
M = 8


def kwadrat(x, y, kolor):
  fillcolor(kolor)
  pu()
  goto(SX + x * BOK, SY + y * BOK)
  pd()
  begin_fill()
  for i in range(4):
    fd(BOK)
    rt(90)
  end_fill()

def kolko(x, y, kolor):
  fillcolor(kolor)

  pu()
  goto(SX + x * BOK + BOK/2, SY + y * BOK - BOK)
  pd()
  begin_fill()
  circle(BOK/2)
  end_fill()

#####################################################

def initial_board():
    B = [ [0] * M for i in range(M)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = -1
    B[4][3] = -1
    return B


class Board:
    dirs = [ (0,1), (1,0), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1) ]


    def __init__(self):
        self.board = initial_board()
        self.fields = set()
        self.move_list = []
        self.history = []
        for i in range(M):
            for j in range(M):
                if self.board[i][j] == 0:
                    self.fields.add( (j,i) )

    def draw(self):
        for i in range(M):
            res = []
            for j in range(M):
                b = self.board[i][j]
                if b == 0:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print()


    def show(self):
        for i in range(M):
            for j in range(M):
                kwadrat(j, i, 'green')

        for i in range(M):
            for j in range(M):
                if self.board[i][j] == 1:
                    kolko(j, i, 'black')
                if self.board[i][j] == -1:
                    kolko(j, i, 'white')

    def moves(self, player):
        res = []
        for (x,y) in self.fields:
            if any( self.can_beat(x,y, direction, player) for direction in Board.dirs):
                res.append( (x,y) )
        if not res:
            return [None]
        return res

    def can_beat(self, x,y, d, player):
        dx,dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x,y) == -player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x,y) == player

    def get(self, x,y):
        if 0 <= x < M and 0 <=y < M:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.history.append([x[:] for x in self.board])
        self.move_list.append(move)

        if move == None:
            return
        x,y = move
        x0,y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx,dy in self.dirs:
            x,y = x0,y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x,y) == -player:
              to_beat.append( (x,y) )
              x += dx
              y += dy
            if self.get(x,y) == player:
                for (nx,ny) in to_beat:
                    self.board[ny][nx] = player

    def result(self):
        res = 0
        for y in range(M):
            for x in range(M):
                b = self.board[y][x]
                if b == -1:
                    res -= 1
                elif b == 1:
                    res += 1
        return res

    def terminal(self):
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def random_move(self, player):
        if player == -1:
            ms = self.moves(player)
            if ms:
                return random.choice(ms)
            return None
        else:
            mozliwe_ruchy = self.moves(player)
            if mozliwe_ruchy == [None]:
                return None
            else:
                wyniki = []
                for r in mozliwe_ruchy:
                    wyniki.append( (minMaxAlfaBeta(Node(self.board,r,player),2,-1000,1000), r) )
                return max(wyniki)[1]

sys.setrecursionlimit(10000)
# f = open('wyniki.txt','w')
porazki = 0
for i in range(1000):
    player = -1
    B = Board()

    while True:
        # print('ruch:',player)
        # B.draw()
        # B.show()
        m = B.random_move(player)
        B.do_move(m, player)
        player = -player
        # input()
        if B.terminal():
            break
    if B.result() < 0:
        porazki += 1
print(porazki)
#     f.write(str(B.result()))
#     f.write('\n')
# f.write('\n')
# f.write('wygranych:',str(res),'\n')
# f.close()
# B.draw()
# B.show()
# print('Result', B.result())
# input('Game over!')


sys.exit(0)
