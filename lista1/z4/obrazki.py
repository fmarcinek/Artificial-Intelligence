
def szukajMaxBloku(obrazek,d):
    maxLiczba = 0
    for i in range(len(obrazek)-d+1):
        x = policzJedynki(obrazek[i:i+d])
        if x > maxLiczba:
            maxLiczba = x
    return maxLiczba

def policzJedynki(obrazek):
    res = 0
    for i in obrazek:
        if i == '1':
            res += 1
    return res

def zamienBity(obrazek,d):
    jedynki = policzJedynki(obrazek)
    x = szukajMaxBloku(obrazek,d)
    return (d - x) + (jedynki - x)

while True:
    obrazek,d = input().split()
    d = int(d)

    print(zamienBity(obrazek,d))
