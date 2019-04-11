from pprint import pprint
import re
import sys

extract_x = re.compile('x=((?P<spread>\d+\.\.\d+)|(?P<single>(\d+)))')
extract_y = re.compile('y=((?P<spread>\d+\.\.\d+)|(?P<single>(\d+)))')

def x_vals(line):
    return match_var(extract_x, line)

def y_vals(line):
    return match_var(extract_y, line)
 
def match_var(extract, line):
    search = re.search(extract, line)
    single = search.group('single')
    spread = search.group('spread')
    if single:  
        return (int(single), int(single))
    else:
        first, second = list(map(int, spread.split('..')))
        if first < second:
            return (first, second)
        else:
            return (second, first)

#with open('simple.txt', 'r') as f:
with open('input.txt', 'r') as f:
    sys.setrecursionlimit(100000)
    ranges = [(x_vals(line), y_vals(line)) for line in f.readlines()]
    x_min = 1000000000
    x_max = -1000000000
    y_min = 1000000000
    y_max = -1000000000
    for r in ranges:
        ((x1, x2), (y1, y2)) = r
        x_min = min(x1, x_min)
        x_max = max(x2, x_max)
        y_min = min(y1, y_min)
        y_max = max(y2, y_max)

    def correct_x(x):
        return x - x_min + 1

    def correct_y(y):
        return y - y_min + 1

    grid = [['.' for _ in range(correct_x(x_max) + 2)] for _ in range(correct_y(y_max) + 2)]
    corrected_ranges = [((correct_x(x1), correct_x(x2)), (correct_y(y1), correct_y(y2))) for ((x1, x2), (y1, y2)) in ranges]

    for bound in corrected_ranges:
        ((x1, x2), (y1, y2)) = bound
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                grid[y][x] = '#'

    def get_fill(x, y):
        return grid[y][x]

    def set_fill(x, y, fill):
        grid[y][x] = fill

    def walled_in(x, y):
        return walled_in_side(x, y, -1) and walled_in_side(x, y, 1)

    def walled_in_side(x, y, delta):
        cur_x = x
        while True:
            cur_fill = get_fill(cur_x, y)
            if cur_fill == '.':
                return False
            elif cur_fill == '#':
                return True
            cur_x += delta

    def fill_row(x, y):
        fill_row_side(x, y, -1)
        fill_row_side(x, y, 1)

    def fill_row_side(x, y, delta):
        cur_x = x
        while get_fill(cur_x, y) != '#':
            set_fill(cur_x, y, '~')
            cur_x += delta

    def print_grid(low=0, high=350):
        print('\n'.join([''.join(row[low:high]) for row in grid]))

    def fill(x, y):
        if y >= correct_y(y_max):
            return
        if get_fill(x, y + 1) == '.':
            set_fill(x, y + 1, '|')
            fill(x, y + 1)
        if get_fill(x, y + 1) in '~#' and get_fill(x + 1, y) == '.':
            set_fill(x + 1, y, '|')
            fill(x + 1, y)
        if get_fill(x, y + 1) in '~#' and get_fill(x - 1, y) == '.':
            set_fill(x - 1, y, '|')
            fill(x - 1, y)
        if walled_in(x, y):
            fill_row(x, y)

    set_fill(correct_x(500), 1, '|')
    fill(correct_x(500), 1)
    print('Part 1', len([tile for row in grid for tile in row if (tile == '|' or tile == '~')]))
    print('Part 2', len([tile for row in grid for tile in row if tile == '~']))
