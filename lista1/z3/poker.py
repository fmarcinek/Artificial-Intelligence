import random

kolory = ['♠','♣','♦','♥']
figury = [str(f) for f in range(2,11)] + ['W','Q','K','A']

talia = [(k,f) for k in kolory for f in figury]

taliaFiguranta = [(k,f) for k in kolory for f in ['W','D','K','A']]
taliaBlotkarza = [(k,f) for k in kolory for f in range(2,11)]

def wylosujKartyFiguranta():
    return random.sample(taliaFiguranta, 5)

def wylosujKartyBlotkarza():
    return random.sample(taliaBlotkarza, 5)

# Figurant zawsze ma przynajmniej dwie takie same figury
# Figurant nigdy nie wylosuje koloru ani strita, ani pokera
def czyBlotkarzWygral(figurant, blotkarz):
    maxFigurant = dajMax(figurant)
    maxBlotkarz = dajMax(blotkarz)

    if maxFigurant == 2:
        # PARA
        if liczbaFigur(figurant) == 4:
            return maxBlotkarz >= 2 and liczbaFigur(blotkarz) != 4
        # 2PARY
        else:
            return maxBlotkarz > 2
    if maxFigurant == 3:
        # TRÓJKA
        if liczbaFigur(figurant) == 3:
            return maxBlotkarz >= 3 and liczbaFigur(blotkarz) != 3
        # FULL
        else:
            return maxBlotkarz == 4 or maPokera(blotkarz)
    if maxFigurant == 4:
        # KARETA
        return maPokera(blotkarz)

def dajMax(karty):
    slownik = {}
    for k in karty:
        fig = k[1]
        if fig in slownik:
            slownik[fig] += 1
        else:
            slownik[fig] = 1
    return max(slownik.values())

def liczbaFigur(karty):
    zbiorFigur = set()
    for k in karty:
        zbiorFigur.add(k[1])
    return len(zbiorFigur)

def maPokera(karty):
    kolory = set()
    figury = []
    for (k,f) in karty:
        kolory.add(k)
        figury.append(f)
    figury.sort()
    return len(kolory) == 1 and inSequence(figury)

def inSequence(liczby):
    for i in range(4):
        if liczby[i]-liczby[i+1] != -1:
            return False
    return True

# mapa = {'♠':2,'♣':3,'♦':5,'♥':7,'2':10,'3':20,'4':30,'5':40,'6':50,'7':60,'8':70, \
#         '9':80,'10':90,'W':100,'Q':110,'K':120,'A':130}
#
# def mapujKartyNaLiczby(karty):
#     return [mapa(k[0])+mapa(k[1]) for k in karty]

def szacuj(liczbaProb):
    wygraneBlotkarza = 0
    for i in range(liczbaProb):
        kartyFiguranta = wylosujKartyFiguranta()
        kartyBlotkarza = wylosujKartyBlotkarza()
        if czyBlotkarzWygral(kartyFiguranta,kartyBlotkarza):
            wygraneBlotkarza += 1
    return wygraneBlotkarza / liczbaProb

if __name__=="__main__":
    with open('blotkarzTests.txt','w') as f:
        f.write("Początkowe testy:\n")
        for i in range(20):
            f.write(str(szacuj(100000))+'\n')
