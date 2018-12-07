from collections import deque, defaultdict
from pprint import pprint

def make_pair(line):
    x, y = line.split(', ')
    return (int(x), int(y))

def next_points(pair):
    x,y = pair
    up = (x, y + 1)
    down = (x, y - 1)
    left = (x - 1, y)
    right = (x + 1, y)
    return [up, down, left, right]

def on_grid(point):
    x, y = point
    return x >= 0 and y >= 0 and x <= max_x and y <= max_y

with open('input.txt', 'r') as f:
    lines = f.readlines()

pairs = [make_pair(line) for line in lines]
max_x = max(map(lambda pair: pair[0], pairs))
max_y = max(map(lambda pair: pair[1], pairs))

grid = [[(None, 1000000000)] * (max_y + 1) for _ in range(max_x + 1)]
queue = deque(list(map(lambda x: (x, x, 0), pairs)))
while len(queue) > 0:
    origin, visit_pt, depth = queue.popleft()
    x, y = visit_pt
    grid_origin, grid_depth = grid[x][y]

    if depth < grid_depth:
        grid[x][y] = (origin, depth)
        for adj_pt in next_points(visit_pt):
            if on_grid(adj_pt):
                queue.append((origin, adj_pt, depth + 1))
    elif depth == grid_depth and not origin == grid_origin:
        grid[x][y] = (None, depth)

#Part 2: Brute Force
def manhattan(pair1, pair2):
    x1, y1 = pair1
    x2, y2 = pair2
    return abs(x1 - x2) + abs(y1 - y2)

count = 0
for i in range(max_x + 1):
    for j in range(max_y + 1):
        if sum([manhattan((i, j), origin) for origin in pairs]) < 10000:
            count += 1
print("Count: ", count)
