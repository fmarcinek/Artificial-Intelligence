import random
from time import time
from obrazki import opt_dist

f = open('zad5_input.txt','r')
n,m = [int(i) for i in f.readline().split()]

xs = []
for i in range(n):
    xs.append(int(f.readline()))

ys = []
for i in range(m):
    ys.append(int(f.readline()))

f.close()


def narysujObrazek(obrazek):
    for wiersz in obrazek:
        print("".join(map(lambda x: '#' if x == 1 else '.',wiersz)))

def zapiszObrazek(obrazek):
    with open('zad5_output.txt','w') as outputFile:
        for wiersz in obrazek:
            outputFile.write("".join(map(lambda x: '#' if x == 1 else '.',wiersz)))
            outputFile.write('\n')

def dajNiepoprawneWiersze(obrazek):
    wiersze = []
    for k in range(len(obrazek)):
        if opt_dist(obrazek[k],xs[k]) > 0:
            wiersze.append(k)
    return wiersze

def dajKolumne(obrazek, k):
    kolumna = []
    for w in obrazek:
        kolumna.append(w[k])
    return kolumna

def dajNiepoprawneKolumny(obrazek):
    kolumny = []
    for k in range(len(obrazek)):
        kol = dajKolumne(obrazek,k)
        if opt_dist(kol,ys[k]) > 0:
            kolumny.append(k)
    return kolumny

def znajdzIndeksDlaWiersza(obrazek,k):
    wiersz = obrazek[k]
    wyniki = []
    for i in range(len(wiersz)):
        if opt_dist(wiersz,xs[k]) > opt_dist(zamien(wiersz,i),xs[k]):
            kol = dajKolumne(obrazek,i)
            if opt_dist(kol,ys[i]) > opt_dist(zamien(kol,k),ys[i]):
                wyniki.append(i)
    if wyniki != []:
        return random.choice(wyniki)
    return random.choice([i for i in range(len(obrazek)) \
                            if opt_dist(wiersz,xs[k]) > opt_dist(zamien(wiersz,i),xs[k])])

def znajdzIndeksDlaKolumny(obrazek,k):
    kolumna = dajKolumne(obrazek,k)
    wyniki = []
    for i in range(len(kolumna)):
        if opt_dist(kolumna,ys[k]) > opt_dist(zamien(kolumna,i),ys[k]):
            wiersz = obrazek[i]
            if opt_dist(wiersz,xs[i]) > opt_dist(zamien(wiersz,k),xs[i]):
                wyniki.append(i)
    if wyniki != []:
        return random.choice(wyniki)
    return random.choice([i for i in range(len(kolumna)) \
                        if opt_dist(kolumna,ys[k]) > opt_dist(zamien(kolumna,i),ys[k])])

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


def rozwiazuj(maxCzas):
    while True:
        obrazek = []
        for i in range(n):
            obrazek.append([0]*m)

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

    narysujObrazek(obrazek)
    zapiszObrazek(obrazek)


if __name__=='__main__':
    rozwiazuj(3)
