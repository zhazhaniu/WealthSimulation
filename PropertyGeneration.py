
import matplotlib.pyplot as pyplot
import numpy as np
import time
import threading
import random
from lfsr import lfsr

PEOPLE_COUNT = 100
ORG_MONEY = 1
SIMULATE_COUNT = 100000
DRAW_PAUSE = 0.1
DRAW_EVERY_COUNT = 500

personMoney = np.linspace(ORG_MONEY, ORG_MONEY, PEOPLE_COUNT)


def innerDraw(i, yMin, yMax, xCoord):
    pyplot.cla()
    pyplot.text(0.5, 1, "Sim Count:%d" % (i,))
    pyplot.ylim(yMin - 1, yMax + 1)
    np.ndarray.sort(personMoney)
    pyplot.bar(xCoord, personMoney)
    pyplot.pause(DRAW_PAUSE)

def innerDraw2(i, yMin, yMax, xCoord):
    pyplot.cla()
    pyplot.text(0.5, 1, "Sim Count:%d" % (i,))
    pyplot.ylim(yMin - 1, yMax + 1)
    partA = np.sort(personMoney[0:int(PEOPLE_COUNT / 2)])
    partB = np.sort(personMoney[int(PEOPLE_COUNT / 2):PEOPLE_COUNT])
    pyplot.bar(xCoord, np.append(partA, np.flip(partB)))
    pyplot.pause(DRAW_PAUSE)


def pyRandom(min, max):
    return random.randint(min, max)


# Every turn, one person random gives one to another, include self
def propertyTranslation(randomMethod):
    pyplot.ion()
    pyplot.ylim(0, 1)
    xCoord = range(PEOPLE_COUNT)
    pyplot.bar(xCoord, personMoney)
    pyplot.pause(1)

    yMin = 1
    yMax = 1

    for i in range(SIMULATE_COUNT - 1):
        # give money
        give = randomMethod(0, PEOPLE_COUNT - 1)
        giveTo = randomMethod(0, PEOPLE_COUNT - 1)
        personMoney[give] -= 1
        yMin = min(personMoney[give], yMin)
        personMoney[giveTo] += 1
        yMax = max(personMoney[giveTo], yMax)

        # draw
        if i % DRAW_EVERY_COUNT == 0:
            innerDraw(i, yMin, yMax, xCoord)


    print(personMoney)
    pyplot.ioff()
    innerDraw(SIMULATE_COUNT, yMin, yMax, xCoord)
    pyplot.pause(60)

# Every turn, one person random gives one to another, include self, but cannot rent money
def propertyTranslation2(randomMethod):
    pyplot.ion()
    pyplot.ylim(0, 1)
    xCoord = range(PEOPLE_COUNT)
    pyplot.bar(xCoord, personMoney)
    pyplot.pause(1)

    yMin = 1
    yMax = 1


    for i in range(SIMULATE_COUNT - 1):
        # give money
        give = randomMethod(0, PEOPLE_COUNT - 1)
        while personMoney[give] <= 0:
            give = randomMethod(0, PEOPLE_COUNT - 1)
        giveTo = randomMethod(0, PEOPLE_COUNT - 1)
        personMoney[give] -= 1
        yMin = min(personMoney[give], yMin)
        personMoney[giveTo] += 1
        yMax = max(personMoney[giveTo], yMax)

        # draw
        if i % DRAW_EVERY_COUNT == 0:
            innerDraw(i, yMin, yMax, xCoord)


    print(personMoney)
    pyplot.ioff()
    innerDraw(SIMULATE_COUNT, yMin, yMax, xCoord)
    pyplot.pause(60)

# Every turn, one person random gives one to another, include self
def propertyTranslation3(randomMethod):
    pyplot.ion()
    pyplot.ylim(0, 1)
    xCoord = range(PEOPLE_COUNT)
    pyplot.bar(xCoord, personMoney)
    pyplot.pause(1)

    yMin = 1
    yMax = 1


    for i in range(SIMULATE_COUNT - 1):
        # give money
        give = randomMethod(0, PEOPLE_COUNT - 1)
        giveTo = randomMethod(0, PEOPLE_COUNT - 1)
        personMoney[give] -= 1
        yMin = min(personMoney[give], yMin)
        personMoney[giveTo] += 1
        yMax = max(personMoney[giveTo], yMax)

        # draw
        if i % DRAW_EVERY_COUNT == 0:
            innerDraw2(i, yMin, yMax, xCoord)


    print(personMoney)
    pyplot.ioff()
    innerDraw2(SIMULATE_COUNT, yMin, yMax, xCoord)
    pyplot.pause(60)


def test1():
    t = threading.Thread(target=propertyTranslation, args=(pyRandom,), daemon=True)
    t.start()
    t.join()
    time.sleep(1)

'''
Mersenne Twister in Python
https://github.com/yinengy/Mersenne-Twister-in-Python
'''
def test2():
    mt = lfsr.Random(int(time.time()))
    def mtRandom(min, max):
        # compatible with random.randint
        return mt.randint(min, max + 1)
    t = threading.Thread(target=propertyTranslation, args=(mtRandom,), daemon=True)
    t.start()
    t.join()
    time.sleep(1)

# another sort method
def test3():
    t = threading.Thread(target=propertyTranslation3, args=(pyRandom,), daemon=True)
    t.start()
    t.join()
    time.sleep(1)

test3()