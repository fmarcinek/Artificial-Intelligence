from collections import deque
from time import time

t0 = time()

wordsDict = {}

with open('words_for_ai1.txt','r') as dictionary:
    for line in dictionary.read().splitlines():
        x = len(line)
        if x in wordsDict:
            wordsDict[x].add(line)
        else:
            wordsDict[x] = {line}
del(wordsDict[0])
wordsDict[1].add('\n')

maxLength = max(wordsDict)

def getExistingWords(index, cost):
    res = []
    for j in range(maxLength,0,-1):
        newIndex = index + j
        if text[index:newIndex] in wordsDict[j]:
            newCost = cost + j**2
            if (newIndex > textLength-1 or textDict[newIndex] != 0 and textDict[newIndex][1] > newCost):
                continue
            textDict[newIndex] = (index, newCost)
            res.append((newIndex,newCost))
    return res

def searchOptimalDivisionOfText():
    queue = deque([(0,0)])
    while queue:
        (index, cost) = queue.pop()
        # print((index, cost))
        newItems = getExistingWords(index, cost)
        queue.extendleft(newItems)

def collectOptimalWords():
    prevIndex = textDict[textLength-1][0]
    if prevIndex == 0:
        raise NameError("\n\nIt's impossible to divide this text into words!")

    res = []
    nextIndex = textLength
    while prevIndex != -1:
        res.append(text[prevIndex:nextIndex])
        nextIndex = prevIndex
        prevIndex = textDict[nextIndex][0]
    res.reverse()
    return res

def setUpSpaces(words):
    return " ".join(words)

if __name__ == '__main__':
    with open('zad2_input.txt') as inputFile:
        text = inputFile.read()
        if not inputFile.read() == "":
            raise NameError('Text file is too large')

    textLength = len(text)
    textDict = [0]*textLength
    textDict[0] = (-1,0)

    searchOptimalDivisionOfText()
    words = collectOptimalWords()
    finalText = setUpSpaces(words)
    t1 = time()
    # with open('zad2_output.txt','w') as output:
    #     output.write(finalText)
    print(finalText)
    print(t1-t0)
