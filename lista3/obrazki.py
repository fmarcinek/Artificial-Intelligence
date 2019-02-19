# 0 - nieznany kolor
# 1 - zamalowany
# 3 - pusty

from collections import deque

with open('zad_input.txt','r') as inputFile:
    n,m = [int(i) for i in inputFile.readline().split()]

    xs = []
    for i in range(n):
        xs.append(list(map(int,inputFile.readline().split())))

    ys = []
    for i in range(m):
        ys.append(list(map(int,inputFile.readline().split())))

def transponuj(n=n,m=m):
    global obrazek
    obrazek = [[obrazek[i][j] for i in range(n)] for j in range(m)]

def odtransponuj():
    transponuj(m,n)

def rysujObrazek(debug=''):
    if debug:
        for wiersz in obrazek:
            print("".join(map(str,wiersz)))
    else:
        for wiersz in obrazek:
            print("".join(map(lambda x: '#' if x == 1 else '.',wiersz)))

def zapiszObrazek():
    with open('zad_output.txt','w') as outputFile:
        for wiersz in obrazek:
            outputFile.write("".join(map(lambda x: '#' if x == 1 else '.',wiersz)))
            outputFile.write("\n")

def spojneBloki(wiersz):
    blok = 0
    res = []
    for w in wiersz:
        if (w == 0 or w == 3):
            if blok != 0:
                res.append(blok)
                blok = 0
        else:
            blok += 1
    if blok != 0:
        res.append(blok)
    if res == []:
        res = [0]
    return res

def dajKolumne(obrazek, k):
    kolumna = []
    for w in obrazek:
        kolumna.append(w[k])
    return kolumna

def poprawny(obrazek):
    return all([spojneBloki(obrazek[i]) == xs[i] for i in range(n)]) \
            and all([spojneBloki(dajKolumne(obrazek, i)) == ys[i] for i in range(m)])

def wszystkieUstawieniaBlokow(num, tryb, ind=0, pos=0):
    # print(num, tryb)
    if tryb == 'w':
        if pos == len(xs[num]):
            return []
        roznica = n - (sum(xs[num])+len(xs[num])-1)
        res = []
        for i in range(roznica+1):
            part = []
            krotszeBloki = wszystkieUstawieniaBlokow(num,tryb,ind+xs[num][pos]+1,pos+1)
            if krotszeBloki == []:
                part = [[(ind+i,xs[num][pos])]]
            else:
                part = [[(ind+i,xs[num][pos])]+x for x in krotszeBloki]
            # print(part)
            res.extend(part)
            # print(res)
        return res
    else:
        if pos == len(ys[num]):
            return []
        roznica = m - (sum(ys[num])+len(ys[num])-1)
        # print(roznica)
        res = []
        # print("ys[num]",ys[num])
        # print("pos:",pos)
        for i in range(roznica+1):
            part = []
            krotszeBloki = wszystkieUstawieniaBlokow(num,tryb,ind+ys[num][pos]+1,pos+1)
            if krotszeBloki == []:
                part = [[(ind+i,ys[num][pos])]]
            else:
                part = [[(ind+i,ys[num][pos])]+x for x in krotszeBloki]
            # print(part)
            res.extend(part)
            # print(res)
        return res

def mozliweUstawieniaBlokow(num, tryb):
    # print(num,tryb,ys[num],wszystkieUstawieniaBlokow(num, tryb))
    bloki = []
    for u in wszystkieUstawieniaBlokow(num, tryb):
        bloki.append(konwertujNaLinie(u,tryb))
    res = []
    for b in bloki:
        if dobryBlok(num, bloki):
            res.append(b)
    return res

def konwertujNaLinie(blok, tryb):
    res = []
    for b in blok:
        for i in range(b[0]-len(res)):
            res.append(3)
        for i in range(b[1]):
            res.append(1)
        res.append(3)
    res.pop()
    if tryb == 'w':
        for i in range(n-len(res)):
            res.append(3)
    else:
        for i in range(m-len(res)):
            res.append(3)
    return res

def dobryBlok(num, blok):
    aktualny = obrazek[num]
    for b,a in zip(blok,aktualny):
        if (b == 3 and a == 1) or (b == 1 and a == 3):
            return False
    return True

def uzupelnij(num,tryb):
    ustawienia = mozliweUstawieniaBlokow(num,tryb)
    return zaznaczPunktyPewne(num,tryb,ustawienia)

def zaznaczPunktyPewne(num,tryb,ustawienia):
    ust = ustawienia[0]
    for i in range(1,len(ustawienia)):
        cos_tam = ustawienia[i]
        for j in range(len(cos_tam)):
            if not ust[j]:
                continue
            if ust[j] != cos_tam[j]:
                ust[j] = False

    res = []
    for i in range(len(ust)):
        if ust[i] and ust[i] != obrazek[num][i]:
            obrazek[num][i] = ust[i]
            res.append(i)
    return [(zamien(tryb),r) for r in res]

def zamien(tryb):
    if tryb == 'k':
        return 'w'
    return 'k'

def rozwiazuj():
    global obrazek
    obrazek = [[0 for i in range(m)] for j in range(n)]

    while not poprawny(obrazek):
        queue = deque([('w',i) for i in range(m)]+[('k',i) for i in range(n)])
        while queue:
            tryb, numer = queue.pop()
            if tryb == 'k':
                transponuj()

            res = uzupelnij(numer,tryb)
            queue.extendleft(res)

            if tryb == 'k':
                odtransponuj()


    rysujObrazek()
    zapiszObrazek()


if __name__=="__main__":
    rozwiazuj()
