from pprint import pprint
import re

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


    grid = [['.' for _ in range(x_max - x_min + 3)] for _ in range(y_max - y_min + 3)]
    corrected_ranges = [((x1 - x_min + 1, x2 - x_min + 1), (y1 - y_min + 1, y2 - y_min + 1)) for ((x1, x2), (y1, y2)) in ranges]

    for bound in corrected_ranges:
        ((x1, x2), (y1, y2)) = bound
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                grid[y][x] = '#'
    #pprint(grid)

#    grid = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
#            ['.', '#', '.', '.', '#', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
#            ['.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.', '.', '.', '.'],
#            ['.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.', '.', '.', '.'],
#            ['.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.'],
#            ['.', '#', '.', '.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '.'],
#            ['.', '#', '#', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '.'],
#            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#            ['.', '.', '.', '.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '.'],
#            ['.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.'],
#            ['.', '.', '.', '.', '#', '.', '.', '.', '#', '.', '#', '.', '.', '.'],
#            ['.', '.', '.', '.', '#', '.', '.', '.', '.', '.', '#', '.', '#', '.'],
#            ['.', '.', '.', '.', '#', '#', '#', '#', '#', '#', '#', '.', '.', '.'],
#            ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]


    def fill(x, y):
        if x > 0 and y > 0 and x < x_max - x_min + 3 and y < y_max - y_min + 3:
            grid[y][x] = '~'

    def is_bounded_grid(x, y):
        sym = grid[y][x]
        return sym == '~' or sym == '#'

    def is_clay_grid(x, y):
        sym = grid[y][x]
        return sym == '#'

    def is_bounded(sym):
        return sym == '~' or sym == '#'

    def spread_water(x_pts, next_pts, x, y):
        for pos, next_pos in zip(x_pts, next_pts):
            fill(pos, y)

            if not is_bounded_grid(pos, y + 1) :
                return [(y, pos)]

            if is_clay_grid(next_pos, y):
                return [(y - 1, x)]

        return []
        

    def flow_out_left(x, y):
        return spread_water(range(x, 1, -1), range(x - 1, 0, -1), x, y)

    def flow_out_right(x, y):
        return spread_water(range(x, len(grid[0]) - 1), range(x + 1, len(grid[0])), x, y)

    def flow_out(x, y):
        left = flow_out_left(x, y)
        right = flow_out_right(x, y)
        flows = left + right

        if flows == []:
            return []
        else:
            max_height = max([y for y, _ in flows])
            return [(y, x) for y, x in flows if y == max_height]

    def flow(water):
        y, x = water

        if is_bounded(grid[y+1][x]):
            fill(x, y)
            return flow_out(x, y)
        else:
            fill(x, y)
            return [(y+1, x)]

    def flow_all_water(water):
        result = []
        for w in water:
            result.extend(flow(w))
        return result

    active_water = [(0, 500 - x_min + 1)]
    while len(active_water) > 0:
        filtered_water = set([(y, x) for y, x in active_water if y < y_max - y_min + 2])
        active_water = flow_all_water(filtered_water)
        #print(active_water)
        #pprint(grid)
        #print()

    print('Part 1: ', len([tile for row in grid for tile in row if tile == '~']))
