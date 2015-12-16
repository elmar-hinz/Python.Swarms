#! /usr/bin/env python

from random import random, sample, randint
from game import BoardGame
from board import Board
from figure import Figure, FigureStrategy

class MoskitoGame(BoardGame):
    def __init__(self, height, width, amount):
        self.board = Board(height, width)
        self.amount = amount

    def setup(self):
        for n in range(self.amount):
            figure = Figure(self.board)
            figure.bindStrategy(MoskitoStrategy())
            figure.strategy.placeIt()
        self.board.figures[0].color = 1

class MoskitoStrategy(FigureStrategy):
    symbol = "."
    deltaX, deltaY = (0, 0)

    def modify(self):
        self.deltaX = randint(-2, 2)
        self.deltaY = randint(-2, 2)

    def placeIt(self):
        x = sample(range(0, self.board.width), 1)[0]
        y = sample(range(0, self.board.height), 1)[0]
        self.modify()
        try:
            self.figure.add(y, x)
        except:
            self.placeIt()

    def planMovement(self):
        if random() < 0.01: self.modify()

    def step(self):
        self.planMovement()
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


