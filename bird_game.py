#! /usr/bin/env python

from random import random, sample, randint
from moskito_game import MoskitoGame, MoskitoStrategy
from figure import Figure
from logger import log
from time import sleep

class BirdGame(MoskitoGame):
    def setup(self):
        for n in range(self.amount):
            figure = Figure(self.board)
            figure.bindStrategy(BirdStrategy())
            figure.strategy.placeIt()
        self.board.figures[0].color = 1

class BirdStrategy(MoskitoStrategy):
    symbol = "-"
    deltaX, deltaY = (1, 1)

    def planMovement(self):
        mnm = self.meanNeighborMovement(len(self.board.figures)/8)
        self.deltaY, self.deltaX = mnm
        if self.deltaY == 0 or self.deltaX == 0:
            self.modify()

    def mean(self, l):
        return int(round(float(sum(l))/len(l)))

    def meanNeighborMovement(self, amount):
        neighbours = self.neighbours(amount)
        deltaX, deltaY = [], []
        for neighbour in neighbours:
            deltaY.append(neighbour.strategy.deltaY)
            deltaX.append(neighbour.strategy.deltaX)
        return (self.mean(deltaY), self.mean(deltaX))

    def neighbours(self, amount):
        neighbours = []
        y, x = self.figure.position()
        radius = 0
        while len(neighbours) < amount:
            radius += 1
            for height in range(y - radius, y + radius + 1):
                for width in range(x - radius, x + radius + 1):
                    try:
                        figure = self.board.figure(height, width)
                        if figure: neighbours.append(figure)
                    except:
                        pass
        neighbours.remove(self.figure)
        return neighbours








