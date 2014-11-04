#!/usr/bin/env python3

import numpy as np

class Robot(object):
    left = {'>': '^', '^': '<', '<': 'v', 'v': '>'}
    right = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
    fwd = {'>': (1, 0), '^': (0, -1), '<': (-1, 0), 'v': (0, 1)}

    def __init__(self, x, y, direction='^'):
        self.x = x
        self.y = y
        self.direction = direction

    def turn_left(self):
        self.direction = self.left[self.direction]

    def turn_right(self):
        self.direction = self.right[self.direction]

    def move_forward(self):
        move = self.fwd[self.direction]
        self.x += move[0]
        self.y += move[1]


class TurtleMaze(object):
    def __init__(self, grid, cards, robot):
        self.grid = grid
        self.cards = cards
        self.robot = robot

    def fetch_star(self):
        self.grid[self.robot.y][self.robot.x] = (
            self.grid[self.robot.y][self.robot.x].lower())

    def run(self):
        stack = []
        function_pointer = 0
        card_pointer = 0
        while True:
            cell = self.grid[self.robot.y][self.robot.x]
            try:
                current_card = self.cards[function_pointer][card_pointer]
            except IndexError:
                if len(stack) > 0:
                    function_pointer, card_pointer = stack.pop(0)
                    continue
                else:
                    raise StopIteration('End of cards')
            card_pointer += 1
            color, direction = current_card[0], current_card[1]
            if color != '.' and color != cell.lower():
                continue
            if direction in '0123456789':
                stack.append((function_pointer, card_pointer))
                function_pointer = int(direction)
                card_pointer = 0
                continue
            if direction == '<':
                self.robot.turn_left()
            elif direction == '>':
                self.robot.turn_right()
            elif direction == '^':
                self.robot.move_forward()
            self.fetch_star()
            if self.check_if_failed():
                raise StopIteration('failed')
            if self.check_if_won():
                raise StopIteration('won')
            yield self

    def check_if_failed(self):
        if self.robot.x < 0 or self.robot.y < 0:
            return True
        try:
            return self.grid[self.robot.y][self.robot.x] == '.'
        except IndexError:
            return True

    def check_if_won(self):
        board = ''.join(''.join(line) for line in self.grid)
        return board == board.lower()

    def __str__(self):
        buffer = []
        for y, line in enumerate(self.grid):
            xbuffer = []
            for x, cell in enumerate(line):
                mark = ' '
                if cell.isupper():
                    mark = '×'
                if self.robot.x == x and self.robot.y == y:
                    mark = self.robot.direction
                xbuffer.append(color(mark, color='white' if mark != '×' else 'yellow',
                                     background={'.': 'black',
                                                 'r': 'red',
                                                 'g': 'green',
                                                 'b': 'blue'}[cell.lower()]))
            buffer.append(''.join(xbuffer))
        return '\n'.join(buffer)


def color(*args, color='white', background='black'):
    """
    Return concatenated *args, colorized by the given `color` parameter.
    `color` take a (red, green, blue) tuple (0-255), or a color name.
    """
    colormap = {'black': (0, 0, 0),
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'yellow': (255, 255, 0),
                'blue': (0, 0, 255),
                'magenta': (255, 0, 255),
                'cyan': (0, 255, 255),
                'white': (255, 255, 255),
                'orange': (255, 165, 0),
                'purple': (128, 0, 128)}
    if type(color) == str:
        color = colormap[color]
    if type(background) == str:
        background = colormap[background]
    return ('\x1b[38;5;%dm\x1b[48;5;%dm' % (
            (16 + (int(color[0] / (255 / 5)) * 36) +
             (int(color[1] / (255 / 5)) * 6) +
             int(color[2] / (255 / 5))),
            (16 + (int(background[0] / (255 / 5)) * 36) +
             (int(background[1] / (255 / 5)) * 6) +
             int(background[2] / (255 / 5)))) +
            ' '.join(args) + '\x1b[0m')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    import sys
    if len(sys.argv) < 2:
        print("Usage: {} game.rz 'cards' ['cards' [...]]".format(sys.argv[0]))
        print(" Cards are tuple of characters, first color (.rgb)")
        print(" second character: direction (<^>) or function number [0-9].")
        print(" No color is dot, so for example ./turtlemaze.py sh.rz 'b^ .> r>'")
        print(" Any cards parameter is a new function, starting with F0.")
        print(" Call a function by its number, like '.0' or 'g2' ...")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        game = f.readlines()
    x, y, direction = game[0].split()
    board = [list(line[:-1]) for line in game[1:]]
    cards = [deck.split(' ') for deck in sys.argv[2:]]
    r = TurtleMaze(board, cards,
                   Robot(int(x), int(y), direction))
    if len(sys.argv) == 2:
        print(r)
        sys.exit(0)
    import time
    for turtlemaze in r.run():
        print(turtlemaze, end="\n\n")
        time.sleep(.2)
    print(r)
    if r.check_if_failed():
        print("You failed !")
    elif r.check_if_won():
        print("You won !")
