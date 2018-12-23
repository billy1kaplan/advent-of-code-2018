from enum import Enum
from pprint import pprint
from collections import Counter

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

textToDirection = {
    '>' : Direction.RIGHT,
    '<' : Direction.LEFT,
    '^' : Direction.UP,
    'v' : Direction.DOWN
}

class SwitchDir(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2

def rotate_right(direction):
    r_dir, c_dir = direction.value
    return Direction((c_dir, -r_dir))

def rotate_left(direction):
    r_dir, c_dir = direction.value
    return Direction((-c_dir, r_dir))

def determine_switch(direction, switch_dir):
    if switch_dir == SwitchDir.LEFT:
        transformation_dir = rotate_left(direction)
    elif switch_dir == SwitchDir.STRAIGHT:
        transformation_dir = direction
    elif switch_dir == SwitchDir.RIGHT:
        transformation_dir = rotate_right(direction)
    return (transformation_dir, SwitchDir((switch_dir.value + 1) % 3))

def read_carts(tracks):
    carts = []

    for row in range(len(tracks)):
        for col in range(len(tracks[row])):
            ch = tracks[row][col]
            if ch in '<>^v':
                carts.append(Cart((row, col), textToDirection[ch]))
    return carts

def read_track(tracks):
    track = {}
    for row in range(len(tracks)):
        for col in range(len(tracks[row])):
            ch = tracks[row][col]
            if ch in '<>':
                track[(row, col)] = '-'
            elif ch in '^v':
                track[(row, col)] = '|'
            else:
                track[(row, col)] = ch
    return track

def handle_corner(direction, corner):
    if corner == '/':
        vert_rotator = rotate_right
        horiz_rotator = rotate_left
    else:
        vert_rotator = rotate_left
        horiz_rotator = rotate_right

    if direction == Direction.UP or direction == Direction.DOWN:
        rotated = vert_rotator(direction)
    else:
        rotated = horiz_rotator(direction)

    x_rot, y_rot = rotated.value
    return ((x_rot, y_rot), rotated)

class Cart(object):
    def __init__(self, pos, direction):
        self.cur_switch = SwitchDir.LEFT
        self.pos = pos
        self.direction = direction

    def advance(self, track, positions):
        x_pos, y_pos = self.pos
        if track in '-|':
            x_t, y_t = self.direction.value
            switch_pos = self.cur_switch
            direction = self.direction
        elif track in '/\\':
            ((x_t, y_t), direction) = handle_corner(self.direction, track)
            switch_pos = self.cur_switch
        elif track == '+':
            direction, switch_pos = determine_switch(self.direction, self.cur_switch)
            x_t, y_t = direction.value
        else:
            raise "Unexpected track type"

        self.pos = (x_pos + x_t, y_pos + y_t)
        self.cur_switch = switch_pos
        self.direction = direction
        if self.pos in positions:
            return self.pos

    def __str__(self):
        return f'Cart at {self.pos}, facing {self.direction}, turning {self.cur_switch}'

class Track(object):
    def __init__(self, tracks={}, carts=[]):
        self.tracks = tracks
        self.carts = carts

    def simulate(self):
        while len(self.carts) > 1:
            #print(self)
            first_crash = self.advance()
            if first_crash:
                return first_crash
        return None

    def advance(self):
        ordered = sorted(self.carts, key = lambda cart: cart.pos)
        for cart in ordered:
            if cart in self.carts:
                positions = set([cart.pos for cart in self.carts])
                row, col = cart.pos
                next_pos = cart.advance(self.tracks[(row, col)], positions)
                if next_pos:
                    self.carts = [safe_cart for safe_cart in self.carts if not safe_cart.pos == next_pos]

    def __str__(self):
        row_max = max([row for row, _ in self.tracks.keys()])
        col_max = max([col for _, col in self.tracks.keys()])

        cartpos = set([cart.pos for cart in self.carts])

        result = [[' ' for _ in range(col_max)] for _ in range(row_max)]
        for r in range(row_max):
            for c in range(col_max):
                if (r, c) in cartpos:
                    result[r][c] = 'X'
                elif (r, c) in self.tracks:
                    result[r][c] = self.tracks[(r, c)]
        return '\n'.join([''.join(row) for row in result])

with open('input.txt', 'r') as f:
    track = f.readlines()
    carts = read_carts(track)
    carts_removed = read_track(track)
    t = Track(carts_removed, carts)
    result = t.simulate()
    #y, x = result
    #print(f'Part 1: ({x}, {y})')
    for cart in t.carts:
        print(cart)
