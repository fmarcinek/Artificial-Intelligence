# 0 - neutralne
# 4 - zamalowane na 100%
# 1 - może zamalowane
# 3 - puste na 100%
# 2 - może puste ???

import random
from time import time

# n,m = [int(i) for i in input().split()]
#
# wiersze = []
# for i in range(n):
#     wiersze.append(list(map(int,input().split())))
#
# kolumny = []
# for i in range(m):
#     kolumny.append(list(map(int,input().split())))

with open('mysz_test.txt','r') as inputFile:
    n,m = [int(i) for i in inputFile.readline().split()]

    xs = []
    for i in range(n):
        xs.append(list(map(int,inputFile.readline().split())))

    ys = []
    for i in range(m):
        ys.append(list(map(int,inputFile.readline().split())))

def zamalujWiersz(w,kolor):
    wiersz = obrazek[w]
    for i in range(m):
        wiersz[i] = kolor

def zamalujPewneWWierszu(w,m,x='w'):
    bloki = []
    if x == 'k':
        bloki = ys[w]
    else:
        bloki = xs[w]
    wiersz = obrazek[w]
    sumaBloku = sum(bloki) + len(bloki) - 1
    if m - sumaBloku < max(bloki):
        r = m - sumaBloku
        index = 0
        for b in bloki:
            if b > r:
                for j in range(index+r, index+b):
                    wiersz[j] = 4
            index += b+1
        if r == 0:
            itr = 0
            index = bloki[0]
            while index < m:
                wiersz[index] = 3
                itr += 1
                index += bloki[itr]+1

def transponuj(n=n,m=m):
    global obrazek
    obrazek = [[obrazek[i][j] for i in range(n)] for j in range(m)]

def odtransponuj():
    transponuj(m,n)


# Żeby pracować na kolumnach trikowo transponujemy obrazek oraz zamieniamy n i m
def znajdzZamalowane(n,m,x='w'):
    w = 0
    for i in range(n):
        if x == 'k':
            w = ys[i]
        else:
            w = xs[i]
        if w[0] == m:
            zamalujWiersz(i,4)
        elif w[0] == 0:
            zamalujWiersz(i,3)
        else:
            zamalujPewneWWierszu(i,m,x)

def rysujObrazek(debug=''):
    if debug:
        for wiersz in obrazek:
            print("".join(map(str,wiersz)))
    else:
        for wiersz in obrazek:
            print("".join(map(lambda x: '#' if x == 4 or x == 1 else '.',wiersz)))

def zapiszObrazek():
    with open('zad_output.txt','w') as outputFile:
        for wiersz in obrazek:
            outputFile.write("".join(map(lambda x: '#' if x == 4 or x == 1 else '.',wiersz)))
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

def dajNiepoprawneWiersze(obrazek):
    wiersze = []
    for k in range(n):
        if spojneBloki(obrazek[k]) != xs[k]:
            wiersze.append(k)
    return wiersze

def dajKolumne(obrazek, k):
    kolumna = []
    for w in obrazek:
        kolumna.append(w[k])
    return kolumna

def dajNiepoprawneKolumny(obrazek):
    kolumny = []
    for k in range(m):
        kol = dajKolumne(obrazek,k)
        if spojneBloki(kol) != ys[k]:
            kolumny.append(k)
    return kolumny

def znajdzIndeksDlaWiersza(obrazek,k):
    wiersz = obrazek[k]
    wyniki = []
    for i in range(len(wiersz)):
        if wiersz[i] == 4 or wiersz[i] == 3:
            continue
        if opt_dist(wiersz,xs[k]) > opt_dist(zamien(wiersz,i),xs[k]):
            kol = dajKolumne(obrazek,i)
            if opt_dist(kol,ys[i]) > opt_dist(zamien(kol,k),ys[i]):
                wyniki.append(i)
    if wyniki != []:
        return random.choice(wyniki)
    wyniki = [i for i in range(len(wiersz)) \
                            if wiersz[i] != 4 and wiersz[i] != 3
                             and opt_dist(wiersz,xs[k]) > opt_dist(zamien(wiersz,i),xs[k])]
    if wyniki != []:
        return random.choice(wyniki)
    return random.choice([i for i in range(len(wiersz)) \
                            if wiersz[i] != 4 and wiersz[i] != 3])

def znajdzIndeksDlaKolumny(obrazek,k):
    kolumna = dajKolumne(obrazek,k)
    wyniki = []
    for i in range(len(kolumna)):
        if kolumna[i] == 4 or kolumna[i] == 3:
            continue
        if opt_dist(kolumna,ys[k]) > opt_dist(zamien(kolumna,i),ys[k]):
            wiersz = obrazek[i]
            if opt_dist(wiersz,xs[i]) > opt_dist(zamien(wiersz,k),xs[i]):
                wyniki.append(i)
    if wyniki != []:
        return random.choice(wyniki)
    wyniki = [i for i in range(len(kolumna)) \
                        if kolumna[i] != 4 and kolumna[i] != 3
                         and opt_dist(kolumna,ys[k]) > opt_dist(zamien(kolumna,i),ys[k])]
    if wyniki != []:
        return random.choice(wyniki)
    return random.choice([i for i in range(len(kolumna)) \
                                if kolumna[i] != 4 and kolumna[i] != 3])

def zamien(lista,k):
    kopia = lista[:]
    kopia[k] = abs(kopia[k]-1)
    return kopia

def zamienPole(obrazek,x,y):
    obrazek[x][y] = abs(obrazek[x][y]-1)

def poprawny(obrazek, zleWiersze, zleKolumny):
    if zleWiersze == [] and zleKolumny == []:
        return True
    return False


def szukajMaxBloku(wiersz,d):
    maxLiczba = 0
    length = len(wiersz)
    for i in range(length-d+1):
        if i != 0 and (i-1 == 1 or i-1 == 4):
            continue
        if i != length-1 and (i+1 == 1 or i+1 == 4):
            continue
        x = policzJedynki(wiersz[i:i+d])
        if x > maxLiczba:
            maxLiczba = x
    return maxLiczba

def policzJedynki(blok):
    res = 0
    for i in blok:
        if i == 1 or i == 4:
            res += 1
    return res

# def opt_dist(wiersz, bloki):
#     wszystkieJedynki = policzJedynki(wiersz)
#     jedynkiWBlokach = 0
#     for b in bloki:
#         jedynkiWBlokach += szukajMaxBloku(wiersz,b)
#     return (sum(bloki) - jedynkiWBlokach) + abs(wszystkieJedynki - jedynkiWBlokach)

def opt_dist(wiersz, bloki):
    # print("OPT_DIST")
    spojneBlokiWWierszu = spojneBloki(wiersz)
    # print("wiersz:",wiersz)
    # print("spójne bloki:",spojneBlokiWWierszu)
    # print("rozwiązanie:",bloki)
    if spojneBlokiWWierszu == []:
        return sum(bloki)
    r = len(spojneBlokiWWierszu) - len(bloki)
    m = min(spojneBlokiWWierszu)
    if r >= 0:
        itr = r
        while itr > 0:
            spojneBlokiWWierszu.remove(min(spojneBlokiWWierszu))
            itr -= 1
        # print("wynik:",r*m + porownajWartosci(bloki,spojneBlokiWWierszu))
        # print("\n\n\n")
        return r*m + porownajWartosci(bloki,spojneBlokiWWierszu)
    # print("wynik:",sum(bloki[:r]) + porownajWartosci(bloki[r:],spojneBlokiWWierszu))
    # print("\n\n\n")
    r *= -1
    return sum(bloki[:r]) + porownajWartosci(bloki[r:],spojneBlokiWWierszu)

def porownajWartosci(bloki, bloki2):
    return sum([abs(bloki[i]-bloki2[i]) for i in range(len(bloki))])

def rozwiazuj(maxCzas):
    while True:
        global obrazek
        obrazek = [[0 for i in range(m)] for j in range(n)]

        znajdzZamalowane(n,m)
        transponuj()
        znajdzZamalowane(m,n,'k')
        odtransponuj()

        startTime = time()
        wybory = ['w','k']
        zleWiersze = []
        zleKolumny = []
        w,k = 0,0

        while time()-startTime < maxCzas:
            zleWiersze = dajNiepoprawneWiersze(obrazek)
            zleKolumny = dajNiepoprawneKolumny(obrazek)

            if poprawny(obrazek,zleWiersze,zleKolumny):
                break

            if (random.choice(wybory) == 'w'):
                if zleWiersze != []:
                    w = random.choice(zleWiersze)
                    k = znajdzIndeksDlaWiersza(obrazek,w)
            else:
                if zleKolumny != []:
                    k = random.choice(zleKolumny)
                    w = znajdzIndeksDlaKolumny(obrazek,k)
            zamienPole(obrazek,w,k)

        if poprawny(obrazek,zleWiersze,zleKolumny):
            break
        print('działał za długo')
    rysujObrazek()
    zapiszObrazek()


if __name__=="__main__":
    rozwiazuj(5)
