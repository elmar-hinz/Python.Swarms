#! /usr/bin/env python

from time import sleep
from logger import log
from strategies import *

class Game():
    @property
    def height(self): return self.board.height

    @property
    def width(self): return self.board.width

    def __init__(self, height, width, amount):
        self.board = Board(height, width)
        self.amount = amount

    def setup(self):
        for n in range(self.amount):
            figure = Figure(self.board)
            figure.strategy = MoskitoFigure(figure)
        self.board.figures()[0].color = 1

    def step(self):
        for figure in self.board.figures(): figure.step()

class Board():
    class TakenException(Exception): pass
    class AboveWidthException(Exception): pass
    class BelowWidthException(Exception): pass
    class AboveHeightException(Exception): pass
    class BelowHeightException(Exception): pass

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.cells = []
        self.positions = dict()
        for y in range(height):
            row = []
            for x in range(width): row.append(None)
            self.cells.append(row)

    def checkPosition(self, y, x):
        if y < 0:  raise Board.BelowHeightException(str(y))
        if x < 0:  raise Board.BelowWidthException(str(x))
        if y >= self.height:  raise Board.AboveHeightException(str(y))
        if x >= self.width:  raise Board.AboveWidthException(str(x))
        if not self.empty(y, x): raise Board.TakenException

    def color(self, y, x):
        figure = self.figure(y, x)
        if figure: return figure.color
        else: return 0

    def add(self, figure, y, x):
        self.checkPosition(y, x)
        self.cells[y][x] = figure
        self.positions[figure] = (y, x)

    def symbol(self, y, x):
        figure = self.figure(y, x)
        if figure: return figure.symbol
        else: return " "

    def empty(self, y, x):
        return self.figure(y, x) == None

    def figure(self, y, x):
        return self.cells[y][x]

    def figures(self):
        return self.positions.keys()

    def move(self, figure, y, x, relative = False):
        oldY, oldX = self.positions[figure]
        if relative:
            y = oldY + y
            x = oldX + x
        self.checkPosition(y, x)
        self.cells[oldY][oldX] = None
        self.cells[y][x] = figure
        self.positions[figure] = (y, x)

    def position(self, figure):
        return self.positions[figure]

class Figure():
    strategy = None
    color = 0
    symbol = "*"

    def __init__(self, board):
        self.board = board

    def add(self, y, x):
        self.board.add(self, y, x)

    def step(self):
        self.strategy.step()

    def position(self):
        return self.board.getPostion(self)

    def move(self, y, x, relative = False):
        self.board.move(self, y, x, relative = relative)


