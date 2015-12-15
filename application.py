#! /usr/bin/env python

import curses
from time import sleep

class Application:

    def __init__(self, screen):
        self.screen = screen
        self.main()

    def main(self):
        self.model = Model(self.screen)
        self.view = View(self.screen)
        self.controller = Controller(self.screen)
        self.wireUp()
        self.loop()

    def wireUp(self):
        pass

    def loop(self):
        self.controller.loop()

class Controller:
    def __init__(self, screen):
        self.screen = screen

    def loop(self):
        self.screen.nodelay(1)
        while True:
            if self.screen.getch() == ord('q'): break
            sleep(0.1)

class Model:
    def __init__(self, screen):
        self.screen = screen

class View:

    def __init__(self, screen):
        self.setupRoot(screen)
        self.setupCanvas()
        self.setupLog()

    def setupRoot(self, screen):
        self.root = screen
        self.root.box()
        self.root.refresh()

    def setupCanvas(self):
        self.canvas = self.child(self.root, 'left')
        self.canvas.box()
        self.canvas.addstr(1, 1, "Canvas")
        self.canvas.refresh()

    def setupLog(self):
        self.log = self.child(self.root, 'right')
        self.log.box()
        self.log.addstr(1, 1, "Log")
        self.log.refresh()

    def child(self, parent, position):
        return curses.newwin(*self.layout(parent, position))

    def layout(self, parent, position):
        y, x = parent.getbegyx()
        height, width = parent.getmaxyx()
        halfHeight = height / 2
        halfWidth = width / 2
        if position == "left":
            return height, halfWidth, y, x
        if position == "right":
            return height, halfWidth, y, x + halfWidth

if __name__ == '__main__':
    curses.wrapper(Application)

