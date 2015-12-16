#! /usr/bin/env python

from logger import log

class Figure():
    strategy = None
    color = 0
    symbol = "*"

    def __init__(self, board):
        self.board = board

    def add(self, y, x):
        self.board.add(self, y, x)

    def injectStrategy(self, strategy):
        strategy.setup(self)
        self.strategy = strategy

    def position(self):
        return self.board.getPostion(self)

    def move(self, y, x, relative = False):
        self.board.move(self, y, x, relative = relative)


class FigureStrategy():
    def setup(self, figure):
        self.figure = figure

    @property
    def board(self):
        return self.figure.board
