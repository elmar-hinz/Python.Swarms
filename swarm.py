#! /usr/bin/env python

import curses.panel, curses, time
from random import *
from time import sleep


amount = 40
width = 80
height = 30
logHeight = 5

class SimpleStrategy:

    def __init__(self, figure):
        self.figure = figure
        self.placeIt()

    def modify(self):
        self.deltaX = randint(-2, 2)
        self.deltaY = randint(-2, 2)

    def move(self):
        if random() < 0.01: self.modify()
        try:
            self.figure.move(self.deltaY, self.deltaX, relative = True)
        except Board.AboveWidthException:
            self.deltaX = -1
        except Board.AboveHeightException:
            self.deltaY = -1
        except Board.BelowWidthException:
            self.deltaX = 1
        except Board.BelowHeightException:
            self.deltaY = 1
        except Board.TakenException:
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
            figure.strategy = SimpleStrategy(figure)
        self.board.figures()[0].color = 1

    def play(self):
        for figure in self.board.figures(): figure.strategy.move()
        return self.board

class Figure():

    strategy = None
    color = 0
    symbol = "*"

    def __init__(self, board):
        self.board = board

    def add(self, y, x):
        self.board.add(self, y, x)

    def position(self):
        return self.board.getPostion(self)

    def move(self, y, x, relative = False):
        self.board.move(self, y, x, relative = relative)

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

class Runner():
    yOffset = 1
    xOffset = 4

    def __init__(self, screen, logHeight, height, width, amount):
        screen.nodelay(1)
        screen.box()
        try: curses.curs_set(0)
        except: pass
        self.screen = screen
        self.game = Game(height, width, amount)
        pan, self.gameWin = self.panel(height, width, self.yOffset, self.xOffset)
        pan2, logWin = self.panel(logHeight, width,
                self.yOffset + height + 2, self.xOffset)
        logger.setup(logWin)
        logger.log("Hit q to quit.")
        curses.panel.update_panels(); self.screen.refresh()
        self.main()

    def main(self):
        for i in range(10): logger.log(i)
        self.game.setup()
        while True:
            if self.screen.getch() == ord('q'): break
            self.draw(self.game.play())
            sleep(0.1)

    def draw(self, board):
        for y in range(self.game.height):
            for x in range(self.game.width):
                curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
                self.gameWin.addstr(y + 1, x + 1,
                        board.symbol(y,x), curses.color_pair(board.color(y,x)))
                curses.panel.update_panels();
                self.screen.refresh()
        curses.panel.update_panels();
        self.screen.refresh()

    def panel(self, h,l, y,x):
        win = curses.newwin(h + 2, l + 2, y, x)
        win.erase(); win.box()
        panel = curses.panel.new_panel(win)
        return panel, win

class Logger:

    msgs = []
    offset = 2

    def setup(self, window):
        self.window = window
        dims = window.getmaxyx()
        self.height, self.width = dims[0] - 2, dims[1] - 2

    def log(self, msg):
        self.msgs.append(str(msg))
        self.draw()

    def draw(self):
        self.window.erase()
        self.window.box()
        lines = self.msgs[-self.height:]
        for n in range(len(lines)):
            self.window.addstr(n + 1, self.offset, lines[n])
        curses.panel.update_panels();
        self.window.refresh()

def stop(x): exit(str(x))

if __name__ == '__main__':
    logger = Logger()
    runner = curses.wrapper(Runner, logHeight, height, width, amount)

