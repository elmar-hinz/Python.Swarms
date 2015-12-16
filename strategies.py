#! /usr/bin/env python

from random import *

class MoskitoFigure:
    def __init__(self, figure):
        self.figure = figure
        self.board = figure.board
        self.placeIt()

    def modify(self):
        self.deltaX = randint(-2, 2)
        self.deltaY = randint(-2, 2)

    def step(self):
        if random() < 0.01: self.modify()
        try:
            self.figure.move(self.deltaY, self.deltaX, relative = True)
        except self.board.AboveWidthException:
            self.deltaX = -1
        except self.board.AboveHeightException:
            self.deltaY = -1
        except self.board.BelowWidthException:
            self.deltaX = 1
        except self.board.BelowHeightException:
            self.deltaY = 1
        except self.board.TakenException:
            self.deltaX = -self.deltaX
            self.deltaY = -self.deltaY

    def placeIt(self):
        x = sample(range(0, self.figure.board.width), 1)[0]
        y = sample(range(0, self.figure.board.height), 1)[0]
        self.modify()
        try:
            self.figure.add(y, x)
        except:
            self.placeIt()

