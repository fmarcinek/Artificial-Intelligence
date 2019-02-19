from itertools import product
from collections import deque
'''julka'''
K = (0,0)
G = []
B = []
ustawione = 0

with open('zad_input.txt','r') as inputFile:
    plansza = []
    numerLinii = -1
    for line in inputFile:
        numerLinii += 1
        for i in range(len(line)):
            pole = line[i]
            if pole == 'W' or pole == '.':
                continue
            elif pole == 'G':
                G.append((numerLinii, i))
            elif pole == 'B':
                B.append((numerLinii, i))
            elif pole == '*':
                B.append((numerLinii, i))
                G.append((numerLinii, i))
                ustawione += 1
            elif pole == 'K':
                K = (numerLinii, i)
        if line == '\n':
            continue
        plansza.append(list(line[:-1]))

for i in plansza:
    print(i)

kierunki = [(-1,0),(1,0),(0,-1),(0,1)]
literki = ['U', 'D', 'L', 'R']
mapaRuchow = {k:l for k,l in zip(kierunki,literki)}
B = tuple(B)
liczbaSkrzynek = len(B)


def neighbours(pos):
    x,y = pos
    return [(x+i,y+j) for (i,j) in kierunki]


def mozliweRuchy(dane):
    K,B,p,u = dane
    if u == liczbaSkrzynek:
        return (True,[])

    ruchy = neighbours(K)
    noweRuchy = []
    for r in ruchy:
        x,y = r
        if plansza[x][y] == 'W':
            continue
        elif r in B:
            newU = u
            kx,ky = K
            newX,newY = (2*x-kx,2*y-ky)
            if plansza[newX][newY] == 'W' or (newX,newY) in B:
                continue
            if (newX,newY) in G:
                newU += 1
            if r in G:
                newU -= 1
            newB = tuple([v for v in B if v != r])
            newB += ((newX,newY),)
            noweRuchy.append((r, newB, dane[:2], newU))
        else:
            noweRuchy.append((r, B, dane[:2], u))
    return (False, noweRuchy)

def zwrocRuch(ruch,pRuch):
    x1,y1 = ruch[0]
    x2,y2 = pRuch[0]
    return mapaRuchow[(x1-x2,y1-y2)]

def zbierzRozwiazanie(ruch, odwiedzone):
    pRuch = odwiedzone[ruch]
    listaRuchow = []
    while pRuch != None:
        listaRuchow.append(zwrocRuch(ruch,pRuch))
        ruch = pRuch
        pRuch = odwiedzone[ruch]
    listaRuchow.reverse()
    return ''.join(listaRuchow)

def zapiszRuchy(ruchy):
    with open('zad_output.txt','w') as outputFile:
        outputFile.write(ruchy+'\n')

def sokobanBFS():
    queue = deque()
    queue.append((K,B,None,ustawione))

    odwiedzone = {}
    itr = 0
    maxIter = 1000000
    while itr < maxIter:
        itr += 1
        ruch = queue.pop()
        if ruch[:2] in odwiedzone:
            continue
        odwiedzone[ruch[:2]] = ruch[2]
        (udaloSie, noweRuchy) = mozliweRuchy(ruch)
        if udaloSie:
            ruchyMagazyniera = zbierzRozwiazanie(ruch[:2], odwiedzone)
            print(ruchyMagazyniera)
            zapiszRuchy(ruchyMagazyniera)
            return ruchyMagazyniera
        queue.extendleft(noweRuchy)
    if itr == maxIter:
        print('Nie ma rozwiązania!')


if __name__ == '__main__':
    sokobanBFS()
