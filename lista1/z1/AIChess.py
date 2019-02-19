from printChess import print_board
from itertools import product
from time import time

def checkMate(bk,wk,wt):
    return isKingAttacked(bk,wk,wt) \
            and all([isAttackedByWhites(x,wk,wt) for x in neighbours(bk)]) \
            and ((not wt in neighbours(bk)) or wt in neighbours(wk))

def isKingAttacked(bk,wk,wt):
    return towerAttacksVertical(bk,wk,wt) or towerAttacksHorizontal(bk,wk,wt)

def towerAttacksHorizontal(bk,wk,wt):
    return (bk[1] == wt[1] and not (wk[1] == wt[1] and isBetween(wk[0],bk[0],wt[0])))

def towerAttacksVertical(bk,wk,wt):
    return (bk[0] == wt[0] and not (wk[0] == wt[0] and isBetween(wk[1],bk[1],wt[1])))

def isBetween(x,y,z):
    if y > z:
        return y > x > z
    else:
        return z > x > y

def isAttackedByWhites(pos,wk,wt):
    return towerAttacksVertical(pos,wk,wt) or towerAttacksHorizontal(pos,wk,wt) \
            or pos in neighbours(wk)

def isAttackedByBlacks(pos,bk):
    return pos in neighbours(bk)

def neighbours(pos):
    (a,b) = pos
    return [(x,y) for (x,y) in product([a-1,a,a+1],[b-1,b,b+1]) \
                                if (x,y) != (a,b) and 1 <= x <= 8 and 1 <= y <= 8]

def mapPosToNumber(pos):
    (let, num) = pos
    return (ord(let) - 96, int(num))

def mapNumbersToLetters(pos):
    (n1,n2) = pos
    return chr(n1+96)+str(n2)

def printBoard(distr):
    (bk,wk,wt) = distr
    bk2 = mapNumbersToLetters(bk)
    wk2 = mapNumbersToLetters(wk)
    wt2 = mapNumbersToLetters(wt)
    print_board(wk2,wt2,bk2)

def whiteKingPossibleMoves(bk,wk,wt):
    return [(bk,pos,wt) for pos in neighbours(wk) \
                                if pos != wt and not isAttackedByBlacks(pos,bk)]

# specyficzna rzecz: czarny król współpracuje => nie może zbić wieży
#                                             => wieża atakuje pole, na którym stoi
def blackKingPossibleMoves(bk,wk,wt):
    return [(pos,wk,wt) for pos in neighbours(bk) \
                             if pos != wt and not isAttackedByWhites(pos,wk,wt)]

def getTowerVerticalMoves(bk,wk,wt):
    (tx,ty) = wt
    (kx,ky) = wk
    if tx == kx:
        if ky > ty:
            return [(tx,y) for y in range(1,ty)] + [(tx,y) for y in range(ty+1,ky)]
        else:
            return [(tx,y) for y in range(ky+1,ty)] + [(tx,y) for y in range(ty+1,9)]
    return [(tx,y) for y in range(1,9) if y != ty]

def getTowerHorizontalMoves(bk,wk,wt):
    (tx,ty) = wt
    (kx,ky) = wk
    if ty == ky:
        if kx > tx:
            return [(x,ty) for x in range(1,tx)] + [(x,ty) for x in range(tx+1,kx)]
        else:
            return [(x,ty) for x in range(kx+1,tx)] + [(x,ty) for x in range(tx+1,9)]
    return [(x,ty) for x in range(1,9) if x != kx]

def whiteTowerPossibleMoves(bk,wk,wt):
    return [(bk,wk,pos) for pos in getTowerVerticalMoves(bk,wk,wt) + getTowerHorizontalMoves(bk,wk,wt)]

def getFoolsMate(fM, bk, wk, wt):
    if checkMate(bk,wk,wt):
        return 0
    queue = []
    if fM == 1:
        queue = blackKingPossibleMoves(bk,wk,wt)
        if queue == []:
            print("ERROR: Sytuacja patowa")
            return
    else:
        queue = whiteKingPossibleMoves(bk,wk,wt) + whiteTowerPossibleMoves(bk,wk,wt)
    return searchFoolsMate(1,fM,set(),queue)

# BFS
def searchFoolsMate(counter, move, visited, queue):
    queue2 = []
    for (bk,wk,wt) in queue:
        if (bk,wk,wt) in visited:
            continue
        visited.add((bk,wk,wt))
        (res, qu) = checkMove(move,bk,wk,wt)
        if res:
            if debug:
                printList.append((bk,wk,wt))
                return (counter,(bk,wk,wt))
            return counter
        queue2.extend(qu)
    res = searchFoolsMate(counter+1, abs(move-1), visited, queue2)

    if debug:
        (count,distr) = res
        prevMove = searchPrevMove(distr,queue)
        printList.append(prevMove)
        return (count,prevMove)
    return res

def searchPrevMove(distr,queue):
    for mov in queue:
        if isPrevOf(mov,distr):
            return mov

def isPrevOf(d1,d2):
    (bk1,wk1,wt1) = d1
    (bk2,wk2,wt2) = d2
    return (bk1 == bk2 and wk1 == wk2 and (wt1[0] == wt2[0] or wt1[1] == wt2[1])) \
        or (bk1 == bk2 and wt1 == wt2 and kingsAreCloser(wk1,wk2)) \
        or (wt1 == wt2 and wk1 == wk2 and kingsAreCloser(bk1,bk2))

def kingsAreCloser(k1,k2):
    (x1,y1) = k1
    (x2,y2) = k2
    return (x1 == x2 and abs(y1-y2) == 1) or (y1 == y2 and abs(x1-x2) == 1) \
        or (abs(x1-x2) == 1 and abs(y1-y2) == 1)

def checkMove(move,bk,wk,wt):
    if checkMate(bk,wk,wt):
        return (True,[])
    if move == 1:
        return (False,whiteKingPossibleMoves(bk,wk,wt) + whiteTowerPossibleMoves(bk,wk,wt))
    return (False,blackKingPossibleMoves(bk,wk,wt))

def prepareInput(inputData):
    (fstMove, wk, wt, bk) = inputData
    fM = 0
    if fstMove == "black":
        fM = 1
    bk2 = mapPosToNumber(bk)
    wk2 = mapPosToNumber(wk)
    wt2 = mapPosToNumber(wt)
    return (fM, bk2, wk2, wt2)

def main(dbg=""):
    global printList
    printList = []
    global debug
    debug = dbg
    (t0,t1) = (0,0)

    f = open('zad1_input.txt','r')
    for line in f:
        t0 = time()
        (firstMove, bk, wk, wt) = prepareInput(line.split())
        print("liczba ruchów:",getFoolsMate(firstMove,bk,wk,wt))
        if debug:
            print()
            print(printList)
            printList.append((bk,wk,wt))
            printList.reverse()
            for move in printList:
                printBoard(move)
            printList = []
            print()
            t1 = time()
            print("Czas:", t1 - t0)
    f.close()

if __name__=="__main__":
    main()
