def in_bounds(pt, grid):  
    x, y = pt
    return x >= 0 and x < len(grid) and y >= 0 and y < len(grid[0])

def adjacent_points(pt):
    x, y = pt
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                yield (x + i, y + j)

def adjacent_symbols(pt, grid):
    x, y = pt
    adj_points = [point for point in adjacent_points(pt) if in_bounds(point, grid)]
    return [get_symbol(point, grid) for point in adj_points]

def get_symbol(pt, grid):
    x, y = pt
    return grid[x][y]

def print_grid(grid):
    print('\n'.join([''.join([item for item in row]) for row in grid]))

def symbol_count(symbols, symbol):
    return len([sym for sym in symbols if sym == symbol])

def advance_point(pt, grid):
    cur_symbol = get_symbol(pt, grid)
    adj_symbols = adjacent_symbols(pt, grid)
    if cur_symbol == '.':
        if symbol_count(adj_symbols, '|') >= 3:
            return '|'
        else:
            return '.'
    elif cur_symbol == '|':
        if symbol_count(adj_symbols, '#') >= 3:
            return '#'
        else:
            return '|'
    elif cur_symbol == '#':
        if symbol_count(adj_symbols, '#') >= 1 and symbol_count(adj_symbols, '|') >= 1:
            return '#'
        else:
            return '.'
    else:
        return 'X'

def advance_grid(grid):
    return [[advance_point((x, y), grid) for y in range(len(grid[x]))] for x in range(len(grid))]

def resource_value(grid):
    symbols = [item for row in grid for item in row] 
    return symbol_count(symbols, '|') * symbol_count(symbols, '#')

def find_cycle(resources):    
    last = resources[-1]
    
    for index, val in enumerate(resources[-2::-1]):
        if val == last:
            return (len(resources) - 1 - index, len(resources) - 1)

with open('input.txt', 'r') as f:
    grid = []
    for line in f.readlines():
        grid.append([ch for ch in line.strip()])

    for i in range(10):
        grid = advance_grid(grid)
    print_grid(grid)
    print('Part 1 = ', str(resource_value(grid)))

with open('input.txt', 'r') as f:
    # SLOW but kind of works
    # Look for a cycle in the resource values, then
    # compute the large iteration based off of the cycle
    grid = []
    for line in f.readlines():
        grid.append([ch for ch in line.strip()])
    resource_values = []
    for i in range(1000):
        resource_values.append(resource_value(grid))
        grid = advance_grid(grid)
    print(resource_values[950:])
    start_cycle, end_cycle = find_cycle(resource_values)
    iterations = 1000000000
    cycle_index = (iterations - start_cycle - 1) % (end_cycle - start_cycle)
    print('Part 2 = ', str(resource_values[start_cycle + cycle_index]))
