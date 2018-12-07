from pprint import pprint

def make_pair(line):
    x, y = line.split(', ')
    return (int(x), int(y))

def next_points(pair):
    x,y = pair
    right = (x + 1, y)
    left = (x - 1, y)
    up = (x, y + 1)
    down = (x, y - 1)
    return [right, left, up, down] 

def on_grid(point):
    x, y = point
    return x >= 0 and y >= 0 and x <= max_x and y <= max_y

with open('input.txt', 'r') as f:
    lines = f.readlines()
    pairs = [make_pair(line) for line in lines]

    max_x = max(map(lambda pair: pair[0], pairs))
    max_y = max(map(lambda pair: pair[1], pairs))

    visited = set()
    hubs = { origin : [origin] for origin in pairs }
    sizes = { origin : 0 for origin in pairs }
    finite_areas = set(pairs) 

grid_size = (max_x + 1) * (max_y + 1)
while len(visited) < grid_size:
    visiting_session = {}
    for origin, queue in hubs.items(): 
        while len(queue) > 0:
            already_visited = queue.pop(0)

            if not on_grid(already_visited):
                if origin in finite_areas:
                    finite_areas.remove(origin)
            elif not already_visited in visited:
                if not already_visited in visiting_session.keys():
                    visiting_session[already_visited] = origin
                else:
                    if not visiting_session[already_visited] == origin:
                        visiting_session[already_visited] = None

    for visited_point, origin in visiting_session.items():
        if origin:
            for next_point in next_points(visited_point):
                hubs[origin].append(next_point)
            visited.add(visited_point)
            sizes[origin] += 1
        else:
            visited.add(visited_point)

max_size = 0
for origin in finite_areas:
    max_size = max(max_size, sizes[origin])
print(max_size)

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
