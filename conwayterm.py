import curses
import random
import sys
import time
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])
CELL_CHAR="o"


def max_dimensions(window):
    height, width = window.getmaxyx()
    return height - 2, width - 1


def random_cell(window):
    width = max_dimensions(window)[1]
    height = max_dimensions(window)[0]
    char = CELL_CHAR
    position_x = random.randrange(1, width)
    position_y = random.randrange(1, height)
    position = Position(position_x, position_y)
    return (position, char)


def will_born(cells, window):
    news = {}
    max_height, max_width = max_dimensions(window)
    for x in range(max_width):
        for y in range(max_height):
            if cells.get(Position(x,y)):
                pass
            else:
                if count_neighbors(Position(x,y), cells) == 3:
                    news[Position(x,y)] = CELL_CHAR
    return news

def count_neighbors(position, cells): #@todo: add window boundaries
    neighbors = 0

    ## left hand corder, clockwise search for neighbors
    if cells.get(Position(position.x-1, position.y-1)):
        neighbors += 1
    if cells.get(Position(position.x, position.y-1)):
        neighbors += 1
    if cells.get(Position(position.x+1, position.y-1)):
        neighbors += 1
    if cells.get(Position(position.x+1, position.y)):
        neighbors += 1
    if cells.get(Position(position.x+1, position.y+1)):
        neighbors += 1
    if cells.get(Position(position.x, position.y+1)):
        neighbors += 1
    if cells.get(Position(position.x-1, position.y+1)):
        neighbors += 1
    if cells.get(Position(position.x-1, position.y)):
        neighbors += 1

    return neighbors

def will_survive(position, cells, window):
    max_height, max_width = max_dimensions(window)
    neighbors = count_neighbors(position, cells)

    return neighbors == 2 or neighbors == 3


def update_cells(prev, window):
    new = {}
    for position, char in prev.items():
        if will_survive(position, prev, window):
            new[position] = char
        
    return {**new, **will_born(prev, window)}


def redisplay(cells, window):
    for position, char in cells.items():
        max_height, max_width = max_dimensions(window)
        if position.y > max_height or position.x >= max_width:
            continue
        window.addch(position.y, position.x, char)



def main(window, speed):
    if curses.can_change_color():
        curses.init_color(curses.COLOR_BLACK, 0,0,0)
        curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
        curses.init_color(curses.COLOR_YELLOW, 1000, 1000, 0)
    try:
        curses.curs_set(0)
    except Exception:
        pass  # Can't hide cursor in 2019 huh?
    cells = {}
    for i in range(10000): # initial population # @todo: make it a portion of height * width
        cell = random_cell(window)
        cells[cell[0]] = cell[1]
        

    while True:
        height, width = max_dimensions(window)
        if len(cells.keys()) >= 0.95 * (height * width):
            cells.clear()
        cells = update_cells(cells, window)

        window.clear()
        redisplay(cells, window)
        window.refresh()
        try:
            time.sleep((0.2) / (speed / 100))
        except ZeroDivisionError:
            time.sleep(0.2)


if __name__ == '__main__':
    speed = 100
    if len(sys.argv) > 1:
        try:
            speed = int(sys.argv[1])
        except ValueError:
            print(
                'Usage:\npython conwayterm.py [SPEED]\n'
                'SPEED is integer representing percents.',
            )
            sys.exit(1)
    try:
        curses.wrapper(main, speed)
    except KeyboardInterrupt:
        sys.exit(0)
